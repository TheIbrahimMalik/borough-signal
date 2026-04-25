"use client";

import { useEffect, useState } from "react";
import {
  getBootstrapData,
  getRecentRuns,
  simulateProposal,
  simulateProposalCompare,
} from "@/lib/api";

type Area = {
  id: { table_name: string; id: string };
  name: string;
  borough_code: string;
  profile: {
    summary: string;
    housing_pressure: string;
    public_transport_dependency: string;
    family_households: string;
    green_space_sensitivity: string;
  };
};

type Segment = {
  id: { table_name: string; id: string };
  name: string;
  attributes: {
    label: string;
    housing: string;
    age_band: string;
    priorities: Record<string, number>;
  };
};

type Issue = {
  id: { table_name: string; id: string };
  name: string;
  description: string;
};

type SimulationResult = {
  area: {
    id: string;
    name: string;
    borough_code: string;
    profile: Record<string, string>;
  };
  proposal_text: string;
  proposal_features?: Record<string, unknown>;
  detected_issues: string[];
  overall_sentiment: string;
  geography_warning: string | null;
  segment_results: Array<{
    segment_id: string;
    segment_name: string;
    label: string;
    stance: string;
    score: number;
    top_issue: string;
    rationale: string;
  }>;
  evidence: Array<{
    id: string;
    title: string;
    snippet: string;
    issue: string;
  }>;
  recommendation: string;
  confidence?: number;
  proposal_id?: string;
  run_id?: string;
  recommendation_id?: string;
};

type ComparisonResult = {
  original: SimulationResult;
  improved_proposal_text: string;
  improved: SimulationResult;
  comparison: {
    overall_sentiment_before: string;
    overall_sentiment_after: string;
    overall_shift: number;
    sentiment_shift: number;
    confidence_before: number;
    confidence_after: number;
    confidence_delta: number;
    support_balance_before: number;
    support_balance_after: number;
    support_balance_delta: number;
    segment_deltas: Array<{
      segment_id: string;
      label: string;
      original_score: number;
      improved_score: number;
      score_delta: number;
      original_stance: string;
      improved_stance: string;
      top_issue_before: string;
      top_issue_after: string;
    }>;
  };
};

type RecentRun = {
  area_id: { table_name: string; id: string };
  confidence: number;
  created_at: string;
  id: { table_name: string; id: string };
  proposal_id: { table_name: string; id: string };
  status: string;
  summary: {
    detected_issues: string[];
    evidence_count: number;
    geography_warning: string | null;
    overall_sentiment: string;
    segment_count: number;
    proposal_text?: string;
    proposal_features?: Record<string, unknown>;
  };
};

type RecentProposal = {
  area_id: { table_name: string; id: string };
  extracted: {
    detected_issues: string[];
    geography_warning: string | null;
  };
  id: { table_name: string; id: string };
  raw_text: string;
  title: string;
};

const SAMPLE_SCENARIOS = [
  {
    label: "Newham housing near Stratford",
    area_id: "newham",
    proposal_text:
      "Build 250 affordable homes near Stratford station with limited parking and new retail space.",
  },
  {
    label: "Southwark tower block trade-off",
    area_id: "southwark",
    proposal_text:
      "Build a 12-storey tower block replacing green space near Elephant and Castle.",
  },
  {
    label: "Hackney safer streets + shops",
    area_id: "hackney",
    proposal_text:
      "Create safer walking routes, better lighting, and small new shops near Shoreditch station.",
  },
  {
    label: "Camden homes near King's Cross",
    area_id: "camden",
    proposal_text:
      "Build 120 affordable homes near King's Cross with reduced parking and better walking access.",
  },
];

export default function Home() {
  const [areas, setAreas] = useState<Area[]>([]);
  const [segments, setSegments] = useState<Segment[]>([]);
  const [issues, setIssues] = useState<Issue[]>([]);
  const [recentRuns, setRecentRuns] = useState<RecentRun[]>([]);
  const [recentProposals, setRecentProposals] = useState<RecentProposal[]>([]);

  const [selectedArea, setSelectedArea] = useState("");
  const [proposalText, setProposalText] = useState("");

  const [loadingBootstrap, setLoadingBootstrap] = useState(true);
  const [simulating, setSimulating] = useState(false);
  const [comparing, setComparing] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<SimulationResult | null>(null);
  const [comparisonResult, setComparisonResult] = useState<ComparisonResult | null>(null);

  async function loadRecentRuns() {
    const data = await getRecentRuns();
    setRecentRuns(data.runs ?? []);
    setRecentProposals(data.proposals ?? []);
  }

  useEffect(() => {
    async function load() {
      try {
        const bootstrap = await getBootstrapData();
        setAreas(bootstrap.areas ?? []);
        setSegments(bootstrap.segments ?? []);
        setIssues(bootstrap.issues ?? []);

        if (bootstrap.areas?.length) {
          setSelectedArea(bootstrap.areas[0].id.id);
        }

        await loadRecentRuns();
      } catch (err) {
        console.error(err);
        setError("Failed to load app data.");
      } finally {
        setLoadingBootstrap(false);
      }
    }

    load();
  }, []);

  async function handleSimulate() {
    if (!selectedArea || !proposalText.trim()) {
      setError("Please choose a borough and enter a proposal.");
      return;
    }

    try {
      setError("");
      setComparisonResult(null);
      setSimulating(true);
      const simulation = await simulateProposal({
        area_id: selectedArea,
        proposal_text: proposalText,
      });
      setResult(simulation);
      await loadRecentRuns();
    } catch (err) {
      console.error(err);
      setError("Failed to run simulation.");
    } finally {
      setSimulating(false);
    }
  }

  async function handleCompare() {
    if (!selectedArea || !proposalText.trim()) {
      setError("Please choose a borough and enter a proposal.");
      return;
    }

    try {
      setError("");
      setComparing(true);
      const comparison = await simulateProposalCompare({
        area_id: selectedArea,
        proposal_text: proposalText,
      });
      setComparisonResult(comparison);
      setResult(comparison.original);
      await loadRecentRuns();
    } catch (err) {
      console.error(err);
      setError("Failed to compare proposal.");
    } finally {
      setComparing(false);
    }
  }

  function handleApplySampleScenario(
    scenario: (typeof SAMPLE_SCENARIOS)[number]
  ) {
    setSelectedArea(scenario.area_id);
    setProposalText(scenario.proposal_text);
    setResult(null);
    setComparisonResult(null);
    setError("");
  }

  function findProposalText(run: RecentRun) {
    return (
      run.summary.proposal_text ??
      recentProposals.find((proposal) => proposal.id.id === run.proposal_id.id)?.raw_text ??
      "Proposal text unavailable."
    );
  }

  function stanceBadgeClass(stance: string) {
    if (stance === "support") {
      return "inline-flex rounded-full border border-green-300 bg-green-50 px-2 py-1 text-xs font-medium text-green-700";
    }
    if (stance === "oppose") {
      return "inline-flex rounded-full border border-red-300 bg-red-50 px-2 py-1 text-xs font-medium text-red-700";
    }
    return "inline-flex rounded-full border border-amber-300 bg-amber-50 px-2 py-1 text-xs font-medium text-amber-700";
    }

  function deltaTextClass(delta: number) {
    if (delta > 0) return "text-sm font-medium text-green-700";
    if (delta < 0) return "text-sm font-medium text-red-700";
    return "text-sm font-medium text-slate-600";
  }

  function prettyLabel(value: string) {
    return value.replaceAll("_", " ");
  }

  function getGraphRows(simulation: SimulationResult) {
    const topSegments = simulation.segment_results.slice(0, 3);

    return topSegments.map((segment) => {
      const citedEvidence =
        simulation.evidence.find((item) => item.issue === segment.top_issue) ??
        simulation.evidence[0];

      return {
        segmentLabel: segment.label,
        topIssue: segment.top_issue,
        evidenceTitle: citedEvidence?.title ?? "No evidence linked",
      };
    });
  }

  function getAddedFeatures() {
    if (!comparisonResult) return [];

    const before = comparisonResult.original.proposal_features ?? {};
    const after = comparisonResult.improved.proposal_features ?? {};

    return Object.keys(after).filter((key) => {
      if (key === "unit_count") return false;
      return !before[key] && Boolean(after[key]);
    });
  }

  function getTopImprovedSegments() {
    if (!comparisonResult) return [];
    return comparisonResult.comparison.segment_deltas
      .filter((item) => item.score_delta > 0)
      .slice(0, 3);
  }

  return (
    <main className="min-h-screen bg-white p-8 text-slate-900">
      <div className="mx-auto max-w-6xl space-y-8">
        <header className="space-y-3">
          <h1 className="text-4xl font-bold">BoroughSignal</h1>
          <p className="text-lg text-slate-600">
            Stateful synthetic audience decision-support system for London planning proposals.
          </p>
        </header>

        {error ? (
          <div className="rounded-xl border border-red-300 bg-red-50 p-4 text-red-700">
            {error}
          </div>
        ) : null}

        <section className="rounded-2xl border p-6 shadow-sm">
          <h2 className="text-2xl font-semibold">Proposal simulator</h2>
          <p className="mt-2 text-sm text-slate-600">
            Choose a borough, describe a proposal, and simulate audience reactions.
          </p>

          <div className="mt-6 grid gap-6 md:grid-cols-2">
            <div className="space-y-2">
              <label htmlFor="borough" className="text-sm font-medium">
                Borough
              </label>
              <select
                id="borough"
                name="borough"
                className="w-full rounded-lg border px-3 py-2"
                value={selectedArea}
                onChange={(e) => setSelectedArea(e.target.value)}
                disabled={loadingBootstrap}
              >
                <option value="" disabled>
                  Select a borough
                </option>
                {areas.map((area) => (
                  <option key={area.id.id} value={area.id.id}>
                    {area.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="space-y-2">
              <label htmlFor="proposal" className="text-sm font-medium">
                Proposal
              </label>
              <textarea
                id="proposal"
                name="proposal"
                rows={5}
                className="w-full rounded-lg border px-3 py-2"
                value={proposalText}
                onChange={(e) => setProposalText(e.target.value)}
                placeholder="Example: Build 250 mixed-use homes near Stratford station with limited parking and new retail space."
              />
            </div>
          </div>

          <div className="mt-6 flex flex-wrap gap-3">
            <button
              onClick={handleSimulate}
              disabled={simulating || comparing || loadingBootstrap}
              className="rounded-lg bg-slate-900 px-4 py-2 text-white disabled:opacity-50"
            >
              {simulating ? "Simulating..." : "Run simulation"}
            </button>

            <button
              onClick={handleCompare}
              disabled={simulating || comparing || loadingBootstrap}
              className="rounded-lg border px-4 py-2 disabled:opacity-50"
            >
              {comparing ? "Comparing..." : "Compare before / after"}
            </button>
          </div>

          <div className="mt-6 space-y-3">
            <div className="text-sm font-medium text-slate-700">Sample scenarios</div>
            <div className="flex flex-wrap gap-2">
              {SAMPLE_SCENARIOS.map((scenario) => (
                <button
                  key={scenario.label}
                  type="button"
                  onClick={() => handleApplySampleScenario(scenario)}
                  className="rounded-full border px-3 py-2 text-sm hover:bg-slate-50"
                >
                  {scenario.label}
                </button>
              ))}
            </div>
          </div>
        </section>

        <section className="grid gap-6 md:grid-cols-2">
          <div className="rounded-2xl border p-6 shadow-sm">
            <h2 className="text-xl font-semibold">Audience segments</h2>
            <div className="mt-4 space-y-3">
              {segments.map((segment) => (
                <div key={segment.id.id} className="rounded-xl border p-4">
                  <div className="font-medium">{segment.attributes.label}</div>
                  <div className="mt-1 text-sm text-slate-600">
                    {segment.attributes.age_band} · {segment.attributes.housing}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-2xl border p-6 shadow-sm">
            <h2 className="text-xl font-semibold">Issue taxonomy</h2>
            <div className="mt-4 space-y-3">
              {issues.map((issue) => (
                <div key={issue.id.id} className="rounded-xl border p-4">
                  <div className="font-medium capitalize">
                    {prettyLabel(issue.name)}
                  </div>
                  <div className="mt-1 text-sm text-slate-600">
                    {issue.description}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {result ? (
          <section className="space-y-6">
            {result.geography_warning ? (
              <div className="rounded-xl border border-amber-300 bg-amber-50 p-4 text-amber-800">
                {result.geography_warning}
              </div>
            ) : null}

            <div className="rounded-2xl border p-6 shadow-sm">
              <h2 className="text-2xl font-semibold">Simulation result</h2>
              <div className="mt-4 grid gap-4 md:grid-cols-4">
                <div className="rounded-xl border p-4">
                  <div className="text-sm text-slate-500">Borough</div>
                  <div className="mt-1 font-medium">{result.area.name}</div>
                </div>
                <div className="rounded-xl border p-4">
                  <div className="text-sm text-slate-500">Overall sentiment</div>
                  <div className="mt-1">
                    <span className={stanceBadgeClass(result.overall_sentiment)}>
                      {result.overall_sentiment}
                    </span>
                  </div>
                </div>
                <div className="rounded-xl border p-4">
                  <div className="text-sm text-slate-500">Detected issues</div>
                  <div className="mt-1 font-medium capitalize">
                    {result.detected_issues.map(prettyLabel).join(", ")}
                  </div>
                </div>
                <div className="rounded-xl border p-4">
                  <div className="text-sm text-slate-500">Signal strength</div>
                  <div className="mt-1 font-medium">
                    {result.confidence ?? "n/a"}
                  </div>
                </div>
              </div>

              {(result.run_id || result.proposal_id) ? (
                <div className="mt-4 rounded-xl border bg-slate-50 p-4 text-sm text-slate-700">
                  <div>Run ID: {result.run_id}</div>
                  <div>Proposal ID: {result.proposal_id}</div>
                </div>
              ) : null}
            </div>

            <div className="grid gap-6 md:grid-cols-2">
              <div className="rounded-2xl border p-6 shadow-sm">
                <h3 className="text-xl font-semibold">Segment reactions</h3>
                <div className="mt-4 space-y-3">
                  {result.segment_results.map((segment) => (
                    <div key={segment.segment_id} className="rounded-xl border p-4">
                      <div className="flex items-center justify-between gap-4">
                        <div className="font-medium">{segment.label}</div>
                        <div className="flex items-center gap-2">
                          <span className={stanceBadgeClass(segment.stance)}>
                            {segment.stance}
                          </span>
                          <span className="text-sm font-medium text-slate-600">
                            {segment.score}
                          </span>
                        </div>
                      </div>
                      <div className="mt-2 text-sm text-slate-600">
                        Top issue: {prettyLabel(segment.top_issue)}
                      </div>
                      <div className="mt-2 text-sm">{segment.rationale}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="space-y-6">
                <div className="rounded-2xl border p-6 shadow-sm">
                  <h3 className="text-xl font-semibold">Evidence</h3>
                  <div className="mt-4 space-y-3">
                    {result.evidence.map((item) => (
                      <div key={item.id} className="rounded-xl border p-4">
                        <div className="font-medium">{item.title}</div>
                        <div className="mt-1 text-sm text-slate-600 capitalize">
                          {prettyLabel(item.issue)}
                        </div>
                        <div className="mt-2 text-sm">{item.snippet}</div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="rounded-2xl border p-6 shadow-sm">
                  <h3 className="text-xl font-semibold">Recommendation</h3>
                  <p className="mt-3 text-sm leading-6 text-slate-700">
                    {result.recommendation}
                  </p>
                </div>
              </div>
            </div>

            <div className="rounded-2xl border p-6 shadow-sm">
              <h3 className="text-xl font-semibold">Knowledge graph view</h3>
              <div className="mt-4 space-y-4">
                <div className="rounded-xl border p-4 text-sm">
                  <span className="font-medium">Proposal</span>
                  <span className="mx-2 text-slate-500">→ affects →</span>
                  <span className="capitalize">
                    {result.detected_issues.map(prettyLabel).join(", ")}
                  </span>
                </div>

                {getGraphRows(result).map((row) => (
                  <div key={`${row.segmentLabel}-${row.topIssue}`} className="rounded-xl border p-4 text-sm space-y-2">
                    <div>
                      <span className="font-medium">{row.segmentLabel}</span>
                      <span className="mx-2 text-slate-500">→ cares about →</span>
                      <span className="capitalize">{prettyLabel(row.topIssue)}</span>
                    </div>
                    <div>
                      <span className="font-medium">Response</span>
                      <span className="mx-2 text-slate-500">→ cites →</span>
                      <span>{row.evidenceTitle}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>
        ) : null}

        {comparisonResult ? (
          <section className="space-y-6 rounded-2xl border p-6 shadow-sm">
            <h2 className="text-2xl font-semibold">Proposal improvement test</h2>

            <div className="grid gap-6 md:grid-cols-2">
              <div className="rounded-xl border p-4">
                <div className="text-sm text-slate-500">Original proposal</div>
                <div className="mt-2 text-sm">{comparisonResult.original.proposal_text}</div>
              </div>

              <div className="rounded-xl border p-4">
                <div className="text-sm text-slate-500">Improved proposal</div>
                <div className="mt-2 text-sm">{comparisonResult.improved_proposal_text}</div>
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-3">
              <div className="rounded-xl border p-4">
                <div className="text-sm text-slate-500">Sentiment shift</div>
                <div className="mt-1 flex items-center gap-2">
                  <span className={stanceBadgeClass(comparisonResult.comparison.overall_sentiment_before)}>
                    {comparisonResult.comparison.overall_sentiment_before}
                  </span>
                  <span className="text-slate-500">→</span>
                  <span className={stanceBadgeClass(comparisonResult.comparison.overall_sentiment_after)}>
                    {comparisonResult.comparison.overall_sentiment_after}
                  </span>
                </div>
              </div>

              <div className="rounded-xl border p-4">
                <div className="text-sm text-slate-500">Signal strength</div>
                <div className="mt-1 font-medium">
                  {comparisonResult.comparison.confidence_before} →{" "}
                  {comparisonResult.comparison.confidence_after}
                </div>
              </div>

              <div className="rounded-xl border p-4">
                <div className="text-sm text-slate-500">Average score delta</div>
                <div className={deltaTextClass(comparisonResult.comparison.overall_shift)}>
                  {comparisonResult.comparison.overall_shift > 0 ? "+" : ""}
                  {comparisonResult.comparison.overall_shift}
                </div>
              </div>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
              <div className="rounded-xl border p-4">
                <h3 className="text-lg font-semibold">Why scores changed</h3>
                <div className="mt-4 space-y-3 text-sm">
                  <div>
                    <div className="font-medium">Added modeled features</div>
                    <div className="mt-1 text-slate-600">
                      {getAddedFeatures().length > 0
                        ? getAddedFeatures().map(prettyLabel).join(", ")
                        : "No new modeled features were added."}
                    </div>
                  </div>

                  <div>
                    <div className="font-medium">Biggest uplift segments</div>
                    <div className="mt-1 text-slate-600">
                      {getTopImprovedSegments().length > 0
                        ? getTopImprovedSegments()
                            .map((item) => `${item.label} (${item.score_delta > 0 ? "+" : ""}${item.score_delta})`)
                            .join(", ")
                        : "No positive segment movement."}
                    </div>
                  </div>

                  <div>
                    <div className="font-medium">Support balance</div>
                    <div className="mt-1 text-slate-600">
                      {comparisonResult.comparison.support_balance_before} →{" "}
                      {comparisonResult.comparison.support_balance_after} (
                      {comparisonResult.comparison.support_balance_delta > 0 ? "+" : ""}
                      {comparisonResult.comparison.support_balance_delta})
                    </div>
                  </div>
                </div>
              </div>

              <div className="rounded-xl border p-4">
                <h3 className="text-lg font-semibold">Interpretation</h3>
                <div className="mt-4 text-sm text-slate-700 leading-6">
                  The improved proposal adds explicit commitments that the parser can model,
                  which changes structured proposal features and shifts segment scores. This
                  makes the before/after comparison auditable rather than purely qualitative.
                </div>
              </div>
            </div>

            <div className="rounded-xl border p-4">
              <h3 className="text-lg font-semibold">Segment deltas</h3>
              <div className="mt-4 space-y-3">
                {comparisonResult.comparison.segment_deltas.map((item) => (
                  <div key={item.segment_id} className="rounded-lg border p-4">
                    <div className="flex items-center justify-between gap-4">
                      <div className="font-medium">{item.label}</div>
                      <div className={deltaTextClass(item.score_delta)}>
                        {item.original_score} → {item.improved_score} (
                        {item.score_delta > 0 ? "+" : ""}
                        {item.score_delta})
                      </div>
                    </div>
                    <div className="mt-2 flex items-center gap-2 text-sm">
                      <span className={stanceBadgeClass(item.original_stance)}>
                        {item.original_stance}
                      </span>
                      <span className="text-slate-500">→</span>
                      <span className={stanceBadgeClass(item.improved_stance)}>
                        {item.improved_stance}
                      </span>
                    </div>
                    <div className="mt-2 text-sm text-slate-600">
                      Top issue: {prettyLabel(item.top_issue_before)} →{" "}
                      {prettyLabel(item.top_issue_after)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>
        ) : null}

        <section className="rounded-2xl border p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-semibold">Recent runs</h2>
            <button
              onClick={loadRecentRuns}
              className="rounded-lg border px-3 py-2 text-sm"
            >
              Refresh
            </button>
          </div>

          <div className="mt-4 space-y-4">
            {recentRuns.length === 0 ? (
              <div className="text-sm text-slate-600">No runs saved yet.</div>
            ) : (
              recentRuns.map((run) => (
                <div key={run.id.id} className="rounded-xl border p-4">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div className="font-medium">{run.id.id}</div>
                    <div className="flex items-center gap-2 text-sm">
                      <span className={stanceBadgeClass(run.summary.overall_sentiment)}>
                        {run.summary.overall_sentiment}
                      </span>
                      <span className="text-slate-600">
                        Signal strength {run.confidence}
                      </span>
                    </div>
                  </div>

                  <div className="mt-2 text-sm text-slate-600">
                    Borough: {run.area_id.id} · Status: {run.status}
                  </div>

                  <div className="mt-2 text-sm text-slate-600">
                    Issues:{" "}
                    {run.summary.detected_issues
                      .map(prettyLabel)
                      .join(", ")}
                  </div>

                  <div className="mt-3 text-sm">{findProposalText(run)}</div>

                  {run.summary.geography_warning ? (
                    <div className="mt-3 rounded-lg border border-amber-300 bg-amber-50 p-3 text-sm text-amber-800">
                      {run.summary.geography_warning}
                    </div>
                  ) : null}
                </div>
              ))
            )}
          </div>
        </section>
      </div>
    </main>
  );
}
