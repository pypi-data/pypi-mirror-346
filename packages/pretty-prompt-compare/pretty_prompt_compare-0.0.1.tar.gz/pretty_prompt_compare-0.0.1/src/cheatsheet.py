from __future__ import annotations
from typing import Any

GRAPH_FIELD_SEP = "<SEP>"

CHEATSHEETS: dict[str, Any] = {}

CHEATSHEETS["cheat_sheet"] = """
In scientific meta-analyses that explore how climate change affects crop yields,
the relationships between variables like crop yield and climate drivers are 
deeply interconnected—and critically shaped by the time and location of the
experiments.

Crops have many type, and each crop exhibits distinct phenological development characteristics
throughout its growth cycle. These developmental stages—such as germination, vegetative growth,
flowering, and maturation—vary in duration and intensity depending on the crop species and
environmental conditions. The differences in phenological development directly influence
the biomass accumulation, resource allocation, and ultimately the formation of yield. As a result,
each crop type produces different levels of yield under given conditions. 

Different crops exhibit distinct yield responses depending on the climate driver they
face, such as elevated temperatures, CO₂ concentrations, drought, or combinations of these.
For instance, crops like wheat and rice tend to show greater sensitivity to heat and CO₂
changes compared to crops like maize and sorghum, which are more resilient in hot, arid
climates. 

The yield outcome also hinges on the timing of exposure to stress—especially during critical
developmental phases like anthesis and grain filling. For example, heat stress during anthesis
can cause a 30% reduction in crop yield, and the reduction is 10% in C4 crops. This highlights
the importance of not only the stress type but also when it occurs within the crop’s lifecycle.

Moreover, the location of an experiment determines the ambient climate baseline, which affects
how far or close conditions are to a crop's optimal temperature range. This regional variability
means that even the same crop can exhibit different yield responses in different climates or
growing zones. For example, a degree of warming that harms yields in one area might have a
neutral or even beneficial effect in another, depending on local conditions.

Importantly, yield response isn’t always driven by single climate factors. The interaction of
multiple stressors—like heat and drought occurring together—often has a more severe effect than
each factor alone. These compound effects can reduce cereal grain yields by up to 60%, compared
to 30–40% for single stress events. Such outcomes can also vary by crop species and depend on
cultivar-specific traits, as well as soil conditions and water availability.

Experimental design adds another layer of complexity. Controlled settings like FACE or open-top
chambers simulate specific climate conditions to isolate variables, but their findings must be
interpreted in the context of real-world environmental variability, where multiple stressors may
co-occur unpredictably.

Ultimately, any accurate interpretation of climate impact on crop yield must take into account
not just the type of crop and climate variable involved, but also where and when the crop was
grown, what combinations of stressors were presentd. These interdependent relationships form the 
backbone of agricultural meta-analysis and are key to projecting how global food systems may evolve 
in a changing climate.
"""

CHEATSHEETS["special_interests"] = """
- Metadata date: This element contains the date on which the metadata was created or updated. The
    date format is YYYY-MM-DD (with hyphens).
- Metadata language: This element records the language in which the metadata is written. It contains
    the code of the language used in the metadata text. Only the three-letter codes from ISO 639-2/B
    (bibliographic codes) should be used, as defined in ISO 639-2. The code for Dutch is "dut".
- Responsible organization metadata: This element contains the name of the organization responsible
    for the metadata. Use the full written name of the responsible organization. An abbreviation may
    be added to the organization name. For correct official government organization names, refer to
    the list of government organizations. Preferably, fill in this element as a gmx:Anchor, where the
    href attribute points to a URI that describes the organization.
    Example: source:
        <Anchor 
        xlink:href="https://www.tno.nl/nl/over-tno/organisatie">
            Nederlandse organisatie voor 
            toegepast-natuurwetenschappelijk onderzoek (TNO)
        </Anchor>
        result: Nederlandse organisatie voor toegepast-natuurwetenschappelijk onderzoek (TNO).
- Landing page: A Web page that can be navigated to in a Web browser to gain access to the catalog, 
    dataset, its distributions and/or additional information.
- Title: A name given to the resource.
- Description: A free-text account of the resource.
- Unique Identifier: A unique identifier of the resource being described or cataloged. The identifier
    is a text string which is assigned to the resource to provide an unambiguous reference within a
    particular context.
- Resource type: The nature or genre of the resource. The value SHOULD be taken from a well governed
    and broadly recognised controlled vocabulary, such as:
        DCMI Type vocabulary [DCTERMS]
        [ISO-19115-1] scope codes
        Datacite resource types [DataCite]
        PARSE.Insight content-types used by re3data.org [RE3DATA-SCHEMA] (see item 15 contentType)
        MARC intellectual resource types
    Some members of these controlled vocabularies are not strictly suitable for datasets or data
    services (e.g., DCMI Type Event, PhysicalObject; [ISO-19115-1] CollectionHardware, CollectionSession,
    Initiative, Sample, Repository), but might be used in the context of other kinds of catalogs defined
    in DCAT profiles or applications.
- Keywords: A keyword or tag describing the resource.
"""

CHEATSHEETS["fill_nightly"] = """---Goal---
Given a list of nightly_entities with metadata and their related source texts, fill in missing fields such as
`entity_name` and `description` for each entity.
Use {language} as output language.

---Steps---
1. For each entity, extract the following information from the text:
- entity_name: A concise, meaningful name based on the source text. If English, capitalize appropriately.
- entity_type: One of the provided types (do not change it).
- description: A short explanation (1 sentence) of what this entity represents or does.

Format each enriched entity as:
("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<description>{tuple_delimiter}<source_id>{tuple_delimiter}<file_path>)

Fill in the `<Nightly Entity Name>` and `<Nightly Inference>` placeholders with actual information or values in the input text.

2. You must output the enriched entities in this format:
("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<description>{tuple_delimiter}<source_id>{tuple_delimiter}<file_path>)

    Use **{record_delimiter}** as the list separator for each entity entry.
    End the output with **{completion_delimiter}**.
    ⚠️ Do **not** use JSON, Python dictionaries, or nested data structures.
    The output must be a **flat string list**, matching the format exactly as shown below.

#############################
---Real Data---
######################
---Data---
Entities: {nightly_entities}
Text:
{input_text}
######################

######################
Output:"""


CHEATSHEETS["nightly_entity_template"] = """
("entity"{tuple_delimiter}"<Nightly Entity Name>"{tuple_delimiter}"Metadata date"{tuple_delimiter}"<Nightly Inference>"){record_delimiter}
("entity"{tuple_delimiter}"<Nightly Entity Name>"{tuple_delimiter}"Metadata language"{tuple_delimiter}"<Nightly Inference>"){record_delimiter}
("entity"{tuple_delimiter}"<Nightly Entity Name>"{tuple_delimiter}"Responsible organization metadata"{tuple_delimiter}"<Nightly Inference>"){record_delimiter}
("entity"{tuple_delimiter}"<Nightly Entity Name>"{tuple_delimiter}"Landing page"{tuple_delimiter}"<Nightly Inference>"){record_delimiter}
("entity"{tuple_delimiter}"<Nightly Entity Name>"{tuple_delimiter}"Title"{tuple_delimiter}"<Nightly Inference>"){record_delimiter}
("entity"{tuple_delimiter}"<Nightly Entity Name>"{tuple_delimiter}"Description"{tuple_delimiter}"<Nightly Inference>"){record_delimiter}
("entity"{tuple_delimiter}"<Nightly Entity Name>"{tuple_delimiter}"Unique Identifier"{tuple_delimiter}"<Nightly Inference>"){record_delimiter}
("entity"{tuple_delimiter}"<Nightly Entity Name>"{tuple_delimiter}"Resource type"{tuple_delimiter}"<Nightly Inference>"){record_delimiter}
("entity"{tuple_delimiter}"<Nightly Entity Name>"{tuple_delimiter}"Keywords"{tuple_delimiter}"<Nightly Inference>"){record_delimiter}
"""