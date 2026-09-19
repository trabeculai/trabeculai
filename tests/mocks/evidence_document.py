import pytest

from trabeculai.retrieval.models import EvidenceDocument


@pytest.fixture
def evidence_documents() -> list[EvidenceDocument]:
    return [
        EvidenceDocument(
            id="hypertension",
            title="Hypertension",
            text=(
                "Hypertension is a condition characterized by elevated blood pressure. "
                "Treatment may include lifestyle changes and antihypertensive medications."
            ),
            source="synthetic",
        ),
        EvidenceDocument(
            id="diabetes",
            title="Diabetes",
            text=(
                "Diabetes mellitus affects blood glucose regulation. "
                "Treatment may include diet, exercise and medication."
            ),
            source="synthetic",
        ),
        EvidenceDocument(
            id="asthma",
            title="Asthma",
            text=(
                "Asthma is a chronic inflammatory airway disease. "
                "Treatment commonly includes inhaled medications."
            ),
            source="synthetic",
        ),
    ]
