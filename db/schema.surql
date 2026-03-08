DEFINE NAMESPACE IF NOT EXISTS boroughsignal;
DEFINE DATABASE IF NOT EXISTS main;

DEFINE TABLE area SCHEMAFULL;
DEFINE FIELD name ON area TYPE string;
DEFINE FIELD borough_code ON area TYPE string;
DEFINE FIELD profile ON area TYPE object FLEXIBLE;

DEFINE TABLE segment SCHEMAFULL;
DEFINE FIELD name ON segment TYPE string;
DEFINE FIELD attributes ON segment TYPE object FLEXIBLE;

DEFINE TABLE persona SCHEMAFULL;
DEFINE FIELD name ON persona TYPE string;
DEFINE FIELD attributes ON persona TYPE object FLEXIBLE;
DEFINE FIELD reasoning_style ON persona TYPE string;

DEFINE TABLE proposal SCHEMAFULL;
DEFINE FIELD title ON proposal TYPE string;
DEFINE FIELD raw_text ON proposal TYPE string;
DEFINE FIELD extracted ON proposal TYPE object FLEXIBLE;
DEFINE FIELD area_id ON proposal TYPE option<record<area>>;

DEFINE TABLE issue SCHEMAFULL;
DEFINE FIELD name ON issue TYPE string;
DEFINE FIELD description ON issue TYPE string;

DEFINE TABLE evidence_doc SCHEMAFULL;
DEFINE FIELD title ON evidence_doc TYPE string;
DEFINE FIELD source_type ON evidence_doc TYPE string;
DEFINE FIELD snippet ON evidence_doc TYPE string;
DEFINE FIELD metadata ON evidence_doc TYPE object FLEXIBLE;

DEFINE TABLE simulation_run SCHEMAFULL;
DEFINE FIELD proposal_id ON simulation_run TYPE option<record<proposal>>;
DEFINE FIELD area_id ON simulation_run TYPE option<record<area>>;
DEFINE FIELD status ON simulation_run TYPE string;
DEFINE FIELD summary ON simulation_run TYPE object FLEXIBLE;
DEFINE FIELD confidence ON simulation_run TYPE float;
DEFINE FIELD created_at ON simulation_run TYPE datetime DEFAULT time::now();

DEFINE TABLE response SCHEMAFULL;
DEFINE FIELD run_id ON response TYPE option<record<simulation_run>>;
DEFINE FIELD persona_id ON response TYPE option<record<persona>>;
DEFINE FIELD stance ON response TYPE string;
DEFINE FIELD rationale ON response TYPE string;
DEFINE FIELD cited_evidence_ids ON response TYPE array;
DEFINE FIELD scores ON response TYPE object FLEXIBLE;

DEFINE TABLE recommendation SCHEMAFULL;
DEFINE FIELD run_id ON recommendation TYPE option<record<simulation_run>>;
DEFINE FIELD original_text ON recommendation TYPE string;
DEFINE FIELD rewritten_text ON recommendation TYPE string;
DEFINE FIELD expected_shift ON recommendation TYPE object FLEXIBLE;

DEFINE TABLE LIVES_IN SCHEMALESS;
DEFINE TABLE BELONGS_TO SCHEMALESS;
DEFINE TABLE CARES_ABOUT SCHEMALESS;
DEFINE TABLE AFFECTS SCHEMALESS;
DEFINE TABLE CITES SCHEMALESS;
