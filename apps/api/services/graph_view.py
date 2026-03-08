from services.surreal import get_db


def get_proposal_graph_view(proposal_id: str) -> dict:
    db = get_db()

    proposal_result = db.query(f"SELECT * FROM proposal:{proposal_id};")
    if not proposal_result:
        raise ValueError(f"Proposal not found: {proposal_id}")

    proposal = proposal_result[0]

    run_result = db.query(
        f"SELECT * FROM simulation_run WHERE proposal_id = proposal:{proposal_id} LIMIT 1;"
    )
    run = run_result[0] if run_result else None

    affect_edges = db.query(f"SELECT * FROM AFFECTS WHERE in = proposal:{proposal_id};")
    issue_ids = [edge["out"].id for edge in affect_edges]

    affected_issues = []
    for issue_id in issue_ids:
        issue_result = db.query(f"SELECT * FROM issue:{issue_id};")
        if issue_result:
            issue = issue_result[0]
            affected_issues.append(
                {
                    "issue_id": issue["id"].id,
                    "issue_name": issue["name"],
                }
            )

    seen_segment_links = set()
    segment_connections = []

    for issue_id in issue_ids:
        care_edges = db.query(f"SELECT * FROM CARES_ABOUT WHERE out = issue:{issue_id};")
        for edge in care_edges:
            segment_id = edge["in"].id
            key = (segment_id, issue_id)
            if key in seen_segment_links:
                continue
            seen_segment_links.add(key)

            segment_result = db.query(f"SELECT * FROM segment:{segment_id};")
            issue_result = db.query(f"SELECT * FROM issue:{issue_id};")

            if segment_result and issue_result:
                segment = segment_result[0]
                issue = issue_result[0]
                segment_connections.append(
                    {
                        "segment_id": segment["id"].id,
                        "segment_label": segment.get("attributes", {}).get("label", segment["name"]),
                        "issue_id": issue["id"].id,
                        "issue_name": issue["name"],
                    }
                )

    cited_evidence = []
    seen_evidence_links = set()

    if run:
        run_id = run["id"].id
        responses = db.query(f"SELECT * FROM response WHERE run_id = simulation_run:{run_id};")

        for response in responses:
            top_issue = response.get("scores", {}).get("top_issue")
            label = response.get("scores", {}).get("label")
            for evidence_ref in response.get("cited_evidence_ids", []):
                evidence_id = evidence_ref.id
                key = (label, evidence_id)
                if key in seen_evidence_links:
                    continue
                seen_evidence_links.add(key)

                evidence_result = db.query(f"SELECT * FROM evidence_doc:{evidence_id};")
                if evidence_result:
                    evidence = evidence_result[0]
                    cited_evidence.append(
                        {
                            "segment_label": label,
                            "top_issue": top_issue,
                            "evidence_id": evidence["id"].id,
                            "evidence_title": evidence["title"],
                        }
                    )

    graph_triples = []

    for issue in affected_issues:
        graph_triples.append(
            f"proposal:{proposal_id} -> AFFECTS -> issue:{issue['issue_id']}"
        )

    for link in segment_connections:
        graph_triples.append(
            f"segment:{link['segment_id']} -> CARES_ABOUT -> issue:{link['issue_id']}"
        )

    for link in cited_evidence:
        graph_triples.append(
            f"response:{link['segment_label']} -> CITES -> evidence:{link['evidence_id']}"
        )

    return {
        "proposal_id": proposal["id"].id,
        "proposal_title": proposal["title"],
        "proposal_text": proposal["raw_text"],
        "affected_issues": affected_issues,
        "segment_connections": segment_connections,
        "cited_evidence": cited_evidence,
        "graph_triples": graph_triples,
    }
