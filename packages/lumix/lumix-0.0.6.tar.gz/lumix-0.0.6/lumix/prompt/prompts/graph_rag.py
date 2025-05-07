from lumix.prompt.template import PromptTemplate


__all__ = [
    "entities_prompt",
    "relations_prompt",
    "entities_prompt_image",
    "relations_prompt_image",
]


template_entities = """Given a text document, your task is to identify and extract all relevant entities \
based on the provided entity types. For each identified entity, please provide the following information \
in a structured format:

**Entity Requirements:**
    1. Entity name: The exact mention in text, properly capitalized
    2. Entity type: Must be one of the specified types: {types}
    3. Description: A detailed summary of the entity's attributes, characteristics, and role in the context
    4. Confidence: A score from 0-10 reflecting certainty about the type classification

**Processing Guidelines:**
    1. Carefully analyze the context around each potential entity
    2. Resolve ambiguous cases by favoring the most contextually appropriate type
    3. Maintain consistency in entity recognition throughout the document
    4. Only include entities that clearly match one of the specified types

**Output Format:**
    Return the results as a Python list of tuples exactly formatted as:
    ```python
    [
        ("EntityName", "EntityType", "Detailed description...", confidence_score),
        ...
    ]
    ```

**Special Cases:**
    1. If no entities are found, return an empty list
    2. For borderline cases (confidence 4-6), include but flag with lower confidence
    3. Omit completely uncertain cases (confidence <4)

**Entity Type Definitions:**
    {types_description}

**Document Content:**
    {content}
    
Please analyze the document and extract all relevant entities according to the above instructions."""

entities_prompt = PromptTemplate(
    input_variables=["types", "content", "types_description"],
    template=template_entities,
)

template_relations = """Given a text document and a list of extracted entities, \
your task is to identify all semantically meaningful relationships between entity pairs. \
Follow these guidelines carefully:

**Relationship Extraction Requirements:**
    1. Source: The origin entity of the relationship (exact name as extracted)
    2. Target: The destination entity of the relationship (exact name as extracted)
    3. Relationship type: Must be one of: {types}
    4. Description: A detailed justification explaining the relationship based on textual evidence
    5. Confidence: Score (0-10) based on:
        - 8-10: Explicitly stated in text
        - 5-7: Strongly implied by context
        - 0-4: Weak or speculative connection

**Processing Rules:**
    1. Only consider relationships where both entities co-occur in the same meaningful context
    2. Ignore trivial co-occurrences without meaningful interaction
    3. Resolve ambiguous cases by selecting the most specific relationship type available

**Output Specification:**
    ```python
    [
        ("SourceEntity", "TargetEntity", "RelationshipType", "Detailed justification...", confidence_score),
        ...
    ]
    ```
    
**Special Cases Handling:**
    1. If no relationships meet confidence threshold (≥5), return empty list

**Relationship Type Definitions:**
    {types_description}

**Document Content:**
    {content}
    
**Extracted Entities:**
    {entities}
    
Please analyze the document and extract all valid relationships according to these instructions."""

relations_prompt = PromptTemplate(
    input_variables=["types_description", "content", "types", "entities"],
    template=template_relations,
)

template_entities_image = """Given multiple images, your task is to identify and extract all relevant entities.
For each identified entity, provide the following information in a structured format:

**Entity Requirements:**
    1. Entity name: The exact visual/textual mention detected, properly capitalized
    2. Entity type: Must be one of the specified types: {types}
    3. Description: A detailed summary of the entity's visual attributes, contextual role, and distinguishing features
    4. Confidence: A score from 0-10 reflecting certainty about the detection and type classification

**Processing Guidelines:**
    1. Analyze both visual content and embedded text in images using multimodal reasoning
    2. For ambiguous cases, use cross-modal context (visual cues + textual references) to determine entity type
    3. Maintain consistency in entity recognition across multiple images of the same entity
    4. Only include entities with clear visual/textual evidence matching specified types

**Output Format:**
    Return results as a Python list of tuples formatted as:
    ```python
    [
        ("EntityName", "EntityType", "Visual/contextual description...", confidence_score),
        ...
    ]
    ```

**Special Cases:**
    1. If no entities are detected, return an empty list
    2. For borderline visual matches (confidence 4-6), include but note lower confidence
    3. Omit cases where visual/textual evidence is unclear (confidence <4)
    4. When entities appear across multiple images, merge entries if they refer to the same canonical entity

**Entity Type Definitions:**
    {types_description}
    
Analyze the provided images to extract relevant entities according to these instructions."""

entities_prompt_image = PromptTemplate(
    input_variables=["types", "types_description"],
    template=template_entities_image,
)

template_relations_image = """Given multiple images and a list of extracted entities, \
your task is to identify all semantically meaningful relationships between entity pairs \
Follow these guidelines carefully:

**Relationship Extraction Requirements:**
    1. Source: Origin entity, exact name as extracted
    2. Target: Destination entity, exact name as extracted
    3. Relationship type: Must be one of: {types}
    4. Description: Justification combining evidence from images
    5. Confidence: Score (0-10) based on:
        - 8-10: Explicit image confirmation
        - 5-7: Strong image support
        - 0-4: Weak correlation

**Processing Rules:**
    1. Analyze relationships across images - entities appearing in different images can have relationships
    2. Consider both:
        - Visual co-occurrence (spatial relationships, recurring visual patterns)
        - Textual co-occurrence (shared captions, labels, embedded text)
    3. Merge relationships that refer to the same canonical connection across images
    4. Ignore relationships without clear visual/textual interaction evidence

**Output Specification:**
    ```python
    [
        ("SourceEntity", "TargetEntity", "RelationshipType", "Visual/textual justification...", confidence_score),
        ...
    ]
    ```

**Special Cases Handling:**
    1. If cross-image entity references are ambiguous, default to per-image relationships
    2. For relationships spanning multiple images, add "(cross-image)" to description
    3. Omit relationships where visual and textual evidence contradict each other

**Relationship Type Definitions:**
    {types_description}

**Extracted Entities:**
    {entities}

Analyze the images to extract meaningful relationships between entities.
"""

relations_prompt_image = PromptTemplate(
    input_variables=["types_description", "types", "entities"],
    template=template_relations_image,
)
