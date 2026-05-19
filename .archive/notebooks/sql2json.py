import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import json
    import csv
    import polars as pl
    from io import StringIO

    return StringIO, mo, pl


@app.cell(hide_code=True)
def _():
    import struct


    def ewkb_point_to_tuple(hex_wkb: str) -> tuple[float, float]:
        """
        Convert a PostGIS EWKB hex string that represents a POINT into a tuple of
        two ``float`` values (x, y).

        Parameters
        ----------
        hex_wkb:
            Hexadecimal string coming directly from a ``bytea`` column, e.g.
            ``'0101000020E6100000CDCCCCCCCCCC2840CDCCCCCCCCCC2840'``.

        Returns
        -------
        (float, float)
            The X and Y coordinates as Python ``float`` (float‑64) values.
        """
        # 1️⃣  Turn the hex representation into raw bytes
        raw = bytes.fromhex(hex_wkb)

        # 2️⃣  Determine endianness
        #    First byte: 0 = big‑endian, 1 = little‑endian (PostGIS always uses little)
        endian_char = "<" if raw[0] == 1 else ">"

        # 3️⃣  Geometry type (4 bytes after the endian byte)
        #    If the high bit 0x20000000 is set the EWKB contains an SRID field.
        geom_type = struct.unpack(endian_char + "I", raw[1:5])[0]

        # 4️⃣  Compute the offset of the first coordinate:
        #    • 1 byte for endian
        #    • 4 bytes for geometry type
        #    • optional 4‑byte SRID (present when 0x20000000 flag is set)
        offset = 1 + 4
        if geom_type & 0x20000000:  # SRID flag present
            offset += 4  # skip the SRID integer

        # 5️⃣  Unpack the two little‑endian double‑precision numbers (8 bytes each)
        x, y = struct.unpack(endian_char + "dd", raw[offset : offset + 16])

        return (x, y)

    return (ewkb_point_to_tuple,)


@app.cell(hide_code=True)
def _(StringIO, ewkb_point_to_tuple, pl):
    """
    Data for Name: website_place; Type: TABLE DATA; Schema: public; Owner: postgres
    """

    _header = "id, slug, title, description, location".split(", ")
    _data = """
    1	piazza-grande	Piazza grande		0101000020E61000005ADA5484FED92540DFE3CF99B1524640
    2	piazza-xx-settembre	Tenda di Piazza XX settembre		0101000020E61000002C71797E1BDA25405535A61D95524640
    3	palazzo-dei-musei	Palazzo dei musei		0101000020E6100000FE2736D8ABD725404F74DA90F9524640
    4	fondazione-san-carlo	Fondazione Collegio San Carlo		0101000020E61000001CD2A8C0C9DA254007AD2C76A0524640
    5	cortile-ex-ospedale-estense	Cortile - ex Ospedale Estense		0101000020E61000000AAAAAD14ED725402E7B8A6CD8524640
    6	palazzo-santa-margherita	Palazzo Santa Margherita		0101000020E61000004CEC747F70DC2540C212A344DE524640
    7	ago-ex-ospedale-santagostino	AGO Modena Fabbriche Culturali (ex Ospedale sant’Agostino)		0101000020E6100000FB76F37DC8D72540D490C26E07534640
    8	gate-26a-via-carteria	Gate 26a (via Carteria)		0101000020E6100000020B6C1685D82540918574D7D2524640
    9	studio-tape-via-carteria	Studio Tape (via Carteria)		0101000020E61000008D97165F6CD8254063807D62C1524640
    10	ammagamma	Ammagamma		0101000020E610000004140E25B5DB2540A7E7B6D149534640
    11	complesso-san-filippo-neri	Complesso San Filippo Neri		0101000020E6100000E62581818BDB2540B53DD9775C534640
    12	complesso-san-paolo	Complesso San Paolo		0101000020E61000007B0601A32FD92540E8062C0051524640
    13	musei-del-duomo-sito-unesco	Musei del Duomo - Sito Unesco		0101000020E6100000D1624A0B03DA2540F8A4140AC4524640
    14	museo-universitario-gemma	Museo Universitario GEMMA		0101000020E6100000BB18B95D1ED92540C2589533CA524640
    15	palazzo-carandini	Palazzo Carandini		0101000020E6100000319CE3935BDA2540B5CD435C6F524640
    16	piazza-matteotti	Piazza Matteotti		0101000020E6100000D87047EE9FD92540818F66D1E0524640
    17	sala-truffaut	Sala Truffaut		0101000020E6100000117B57F3D2D72540BDD41929A5524640
    18	centro-culturale-g-alberione	Centro Culturale G. Alberione		0101000020E61000002B04377664DB2540BB90F1841F534640
    19	foro-boario	Foro Boario		0101000020E6100000D5F99592F3D72540D19232602E534640
    20	galleria-d406	Galleria D406		0101000020E6100000B3BC8572F6D82540F72C465719534640
    21	pomposa	Pomposa		0101000020E6100000A9D910F650D92540A2540CA114534640
    22	teatro-storchi	Teatro Storchi		0101000020E6100000347C327EB8DC254070E591E45E524640
    """

    places = pl.read_csv(
        StringIO(_data.strip()), separator="\t", has_header=False, new_columns=_header
    )
    places = places.with_columns(
        pl.col("location")
        .map_elements(ewkb_point_to_tuple, return_dtype=list[float])
        .alias("coordinates"),
    ).with_columns(
        pl.col("coordinates").list.get(0).alias("longitude"),
        pl.col("coordinates").list.get(1).alias("latitude"),
    )
    places
    return (places,)


@app.cell(hide_code=True)
def _(StringIO, pl):
    """
    Data for Name: website_word; Type: TABLE DATA; Schema: public; Owner: postgres
    """

    _header = "id, text, visible".split(", ")
    _data = """
    50	sorpresa	t
    3	2023	t
    5	scoprire	t
    6	piazza	t
    8	racchiudere	t
    94	pietra	t
    9	nsieme	t
    10	imponente	t
    11	cominciare	t
    51	precisione	t
    1	festival	t
    52	geometria	t
    13	stampa	t
    14	trascrizione	t
    95	guglie	t
    16	sentimento	t
    96	bianco	t
    19	ricerca	t
    20	sembrare	t
    21	tuffo	t
    22	altro	t
    53	stupendo	t
    24	anima	t
    25	architetto	t
    26	esaltare	t
    27	partecipazione	t
    28	cultura	t
    29	condivisione	t
    30	comunicare	t
    31	comunicazione	t
    32	equo	t
    33	sostenibile	t
    34	confine	t
    35	suv	t
    36	stanchezza	t
    37	giardino	t
    38	segreto	t
    39	pieno	t
    40	meraviglia	t
    41	tristezza	t
    42	cesarini	t
    43	misura	t
    54	giulia	t
    134	camminare	t
    44	metafisico	t
    45	collettivo	t
    46	melodia	t
    47	misterioso	t
    48	profondo	t
    49	passione	t
    55	napoleone	t
    56	fantastico	t
    57	confort	t
    58	zona	t
    59	dare	t
    18	comunità	t
    61	via	t
    62	carteria	t
    63	musica	t
    7	storia	t
    64	culturo	t
    15	abitare	t
    65	vivere	t
    129	desidero	t
    67	consapevolezza	t
    68	rinnovato	t
    69	presente	t
    70	circondare	t
    71	volere	t
    72	esserci	t
    73	sveva	t
    4	luogo	t
    17	accoglienza	t
    74	lentezza	t
    75	riposo	t
    76	risuonare	t
    77	mente	t
    78	attivo	t
    79	libri	t
    80	sacro	t
    81	avere	t
    82	bisogno	t
    83	informazione	t
    84	capire	t
    85	tecnologia	t
    86	piacere	t
    87	pensare	t
    89	ritorno	t
    90	semplicità	t
    97	testa	t
    98	reclinato	t
    91	sole	t
    92	splendere	t
    2	filosofia	t
    93	musi	t
    99	tendere	t
    100	orecchia	t
    102	curioso	t
    103	fotografia	t
    118	sentire	t
    106	quotidiano	t
    107	fratellanza	t
    108	simpatia	t
    109	muro	t
    110	graffito	t
    104	arte	t
    111	effimero	t
    112	architetturo	t
    113	lettura	t
    114	semiotico	t
    105	vita	t
    88	essere	t
    115	rumore	t
    116	solito	t
    117	riesco	t
    119	connessione	t
    120	città	t
    121	cuore	t
    12	parola	t
    122	crociato	t
    123	magia	t
    124	apparizione	t
    125	dissolvenza	t
    126	polvere	t
    127	miracolo	t
    66	spazio	t
    128	civile	t
    130	avverare	t
    131	luce	t
    23	tempo	t
    101	attesa	t
    132	strada	t
    133	sedere	t
    135	rifugio	t
    60	voce	t
    136	allegro	t
    137	armonico	t
    138	bellezza	t
    """
    words = pl.read_csv(
        StringIO(_data.strip()), separator="\t", has_header=False, new_columns=_header
    )
    return (words,)


@app.cell(hide_code=True)
def _(StringIO, pl):
    """
    Data for Name: website_wordfrequency; Type: TABLE DATA; Schema: public; Owner: postgres
    """

    _header = "id, word_id, frequency, place_id".split(", ")
    _data = """
    51	50	1	5
    3	3	1	1
    4	4	1	1
    5	5	1	1
    6	6	1	1
    8	8	1	1
    84	80	1	3
    9	9	1	1
    10	10	1	12
    11	11	1	1
    52	51	1	3
    1	1	3	1
    53	52	1	3
    13	13	1	8
    14	14	1	8
    15	15	1	16
    16	16	1	16
    17	17	1	16
    18	18	1	1
    19	19	1	8
    20	20	1	1
    21	21	1	1
    22	22	1	1
    23	23	1	1
    24	24	1	1
    25	25	1	1
    26	26	1	1
    54	53	1	3
    27	27	2	1
    28	28	1	1
    29	29	1	1
    30	30	1	1
    31	31	1	2
    32	32	1	2
    33	33	1	2
    34	34	1	3
    35	35	1	21
    36	36	1	4
    37	37	1	5
    38	38	1	5
    39	39	1	5
    40	40	1	5
    41	41	1	1
    42	42	1	5
    43	43	1	5
    44	23	2	5
    45	44	1	5
    46	45	1	5
    47	46	1	5
    48	47	1	5
    49	48	1	5
    50	49	1	5
    55	54	1	3
    56	55	1	3
    57	56	1	3
    58	57	1	8
    59	58	1	8
    60	59	1	1
    61	60	1	1
    85	81	1	16
    62	61	1	8
    63	62	1	8
    64	63	1	1
    12	12	5	1
    7	7	3	1
    65	64	1	1
    66	15	1	1
    67	65	1	1
    69	67	1	1
    70	68	1	1
    71	69	1	1
    72	70	1	1
    73	71	1	1
    74	72	1	1
    75	73	1	1
    76	4	1	19
    77	17	1	19
    78	74	1	19
    79	75	1	19
    80	76	1	1
    81	77	1	1
    82	78	1	1
    83	79	1	3
    86	82	1	16
    87	83	1	16
    88	84	1	16
    89	85	1	16
    90	86	1	16
    91	87	1	16
    92	88	1	16
    93	89	1	16
    94	90	1	16
    99	95	1	1
    100	96	1	1
    95	91	2	1
    96	92	2	1
    2	2	5	1
    97	93	1	1
    98	94	1	1
    101	97	1	1
    102	98	1	1
    103	99	1	1
    104	100	1	1
    105	101	1	4
    106	102	1	4
    107	103	1	6
    108	104	1	6
    109	105	1	6
    110	106	1	6
    111	107	1	1
    112	108	1	3
    113	109	1	5
    114	110	1	5
    115	104	1	5
    116	111	1	5
    117	112	1	5
    118	113	1	5
    119	114	1	5
    120	105	1	5
    121	88	1	13
    122	115	1	13
    123	116	1	13
    124	117	1	13
    125	118	1	13
    126	119	1	13
    68	66	2	1
    127	120	1	13
    128	121	1	13
    129	12	1	5
    130	122	1	5
    131	123	1	12
    132	124	1	12
    133	125	1	12
    134	126	1	12
    135	127	1	12
    136	128	1	1
    137	129	1	12
    138	130	1	12
    139	131	1	12
    140	23	1	12
    141	101	1	12
    142	132	1	12
    143	133	1	12
    144	134	1	12
    145	135	1	12
    146	60	1	12
    147	136	1	12
    148	18	1	12
    149	137	1	12
    150	138	1	12
    """

    frequencies = pl.read_csv(
        StringIO(_data.strip()), separator="\t", has_header=False, new_columns=_header
    )
    return (frequencies,)


@app.cell
def _(frequencies, pl, places, titled, words):
    _frequencies = frequencies.with_columns(
        pl.col("word_id")
        .map_elements(lambda v: words.filter(pl.col("id") == v)["text"].item())
        .alias("word")
    ).select("place_id", "word", "frequency")

    out = []
    for _id, _lat, _lon in places.select("id", "latitude", "longitude").iter_rows():
        out.append(
            {
                "coordinates": [_lat, _lon],
                "frequencies": [
                    [_word.title() if titled.value else _word, _freq]
                    for _, _word, _freq in _frequencies.filter(
                        pl.col("place_id") == _id
                    ).iter_rows()
                ],
            }
        )

    out
    return


@app.cell
def _(mo):
    titled = mo.ui.checkbox(label="title words", value=False)
    titled
    return (titled,)


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
