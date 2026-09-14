# KIproBatt manufacturing data

Source: **KIproBatt/kiprobatt-dataset v0.3.2**, [Zenodo release 11895571](https://zenodo.org/records/11895571),
[source repository](https://github.com/KIproBatt/kiprobatt-dataset),
[project and knowledge platform](https://kiprobatt.de/wiki).

Creators credited by the release: Simon P. Stier, Andreas Gronbach, Xukuan Xu,
Andreas Räder, Jonas Rodi, Kai Oppel, Franziska Stahl, Jannis Johann,
Thilo Zürrlein and Lukas Gold.

License: [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
The source data describes laboratory-scale battery manufacturing.

The importer downloads the pinned archive, verifies the publisher's MD5
`03dbcb62fcf17f843b90709d07668450`, and parses the JSON-LD with RDFLib after cp1252 decoding.
Original RDF identifiers and source filenames are retained. The Neo4j projection assigns stable
hashed UIDs, extracts object-specific predecessor relations, and parses Maccor cycle tables with
decimal commas. These transformations are made by BatteryCopilot; the source creators do not
endorse its generated reports. Generated answers and user review notes are not original dataset records.

Measured import contents: 786 JSON-LD files, 256,980 RDF triples, 24,577 source subjects
(718 process instances, 1,574 steps, 17,736 parameters, 4,549 objects), and 108 cycle-statistics files.
The statistics are linked to 109 graph objects: one file is referenced by two objects.
These counts do **not** establish 109 independent physical cells or 718 completed production runs.
The importer also recognizes the source filename ending in `-STATS--.txt`.

In this projection, 103 test-linked objects have three object stages in their explicit predecessor
trace, one has four stages, and five have only the current object. Those paths reach 126 process
instances. This describes graph coverage, not validation of complete physical manufacturing histories.

The archive contains 121 test text files in `files/`; this iteration parses the 108 cycle-statistics
exports. The other 13 exports and externally linked images are not incorporated into test analysis.
Unfilled parameter values remain missing, and upstream connections are not inferred from batch membership.

Archive downloads stay local and are ignored by Git. Reproduce the import with:

```powershell
uv run python -m battery_copilot.manufacturing_ingest
```
