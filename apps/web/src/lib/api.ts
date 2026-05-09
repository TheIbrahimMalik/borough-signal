export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8001";

export async function getBootstrapData() {
  const res = await fetch(`${API_BASE_URL}/lookups/bootstrap`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch bootstrap data: ${res.status}`);
  }

  return res.json();
}

export async function simulateProposal(input: {
  area_id: string;
  proposal_text: string;
}) {
  const res = await fetch(`${API_BASE_URL}/simulate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(input),
  });

  if (!res.ok) {
    throw new Error(`Failed to simulate proposal: ${res.status}`);
  }

  return res.json();
}

export async function simulateProposalCompare(input: {
  area_id: string;
  proposal_text: string;
}) {
  const res = await fetch(`${API_BASE_URL}/simulate/compare`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(input),
  });

  if (!res.ok) {
    throw new Error(`Failed to compare proposal: ${res.status}`);
  }

  return res.json();
}

export async function getRecentRuns() {
  const res = await fetch(`${API_BASE_URL}/runs/recent`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch recent runs: ${res.status}`);
  }

  return res.json();
}
