-- Areas
CREATE area:camden CONTENT {
  name: "Camden",
  borough_code: "E09000007",
  profile: {
    housing_pressure: "high",
    public_transport_dependency: "high",
    family_households: "moderate",
    green_space_sensitivity: "moderate",
    summary: "Dense inner London borough with high housing pressure and strong public transport usage."
  }
};

CREATE area:newham CONTENT {
  name: "Newham",
  borough_code: "E09000025",
  profile: {
    housing_pressure: "high",
    public_transport_dependency: "high",
    family_households: "moderate",
    green_space_sensitivity: "moderate",
    summary: "Fast-changing borough with high housing demand, strong commuter dependence, and mixed tenure patterns."
  }
};

CREATE area:southwark CONTENT {
  name: "Southwark",
  borough_code: "E09000028",
  profile: {
    housing_pressure: "high",
    public_transport_dependency: "high",
    family_households: "moderate",
    green_space_sensitivity: "moderate",
    summary: "Dense borough with major regeneration zones and varied local housing pressures."
  }
};

CREATE area:westminster CONTENT {
  name: "Westminster",
  borough_code: "E09000033",
  profile: {
    housing_pressure: "high",
    public_transport_dependency: "high",
    family_households: "low",
    green_space_sensitivity: "high",
    summary: "Central borough with intense transport flows, mixed commercial use, and strong local character concerns."
  }
};

CREATE area:hackney CONTENT {
  name: "Hackney",
  borough_code: "E09000012",
  profile: {
    housing_pressure: "high",
    public_transport_dependency: "high",
    family_households: "moderate",
    green_space_sensitivity: "high",
    summary: "Popular inner London borough with strong community identity and sensitivity to affordability pressures."
  }
};

-- Segments
CREATE segment:young_renters CONTENT {
  name: "young_renters",
  attributes: {
    label: "Young renters",
    housing: "private_renter",
    age_band: "25-34",
    priorities: {
      affordability: 0.9,
      transport: 0.8,
      green_space: 0.5,
      safety: 0.6,
      local_character: 0.3
    }
  }
};

CREATE segment:family_renters CONTENT {
  name: "family_renters",
  attributes: {
    label: "Family renters",
    housing: "renter",
    age_band: "30-49",
    priorities: {
      affordability: 0.9,
      transport: 0.6,
      green_space: 0.7,
      safety: 0.8,
      local_character: 0.4
    }
  }
};

CREATE segment:homeowners CONTENT {
  name: "homeowners",
  attributes: {
    label: "Homeowners",
    housing: "owner_occupier",
    age_band: "35-64",
    priorities: {
      affordability: 0.4,
      transport: 0.5,
      green_space: 0.6,
      safety: 0.7,
      local_character: 0.8
    }
  }
};

CREATE segment:commuters CONTENT {
  name: "commuters",
  attributes: {
    label: "Commuters",
    housing: "mixed",
    age_band: "25-54",
    priorities: {
      affordability: 0.5,
      transport: 0.95,
      green_space: 0.3,
      safety: 0.5,
      local_character: 0.3
    }
  }
};

CREATE segment:older_residents CONTENT {
  name: "older_residents",
  attributes: {
    label: "Older residents",
    housing: "mixed",
    age_band: "60+",
    priorities: {
      affordability: 0.4,
      transport: 0.5,
      green_space: 0.6,
      safety: 0.8,
      local_character: 0.7
    }
  }
};

CREATE segment:local_business_workers CONTENT {
  name: "local_business_workers",
  attributes: {
    label: "Local business workers",
    housing: "mixed",
    age_band: "25-54",
    priorities: {
      affordability: 0.6,
      transport: 0.7,
      green_space: 0.4,
      safety: 0.6,
      local_character: 0.5
    }
  }
};

-- Issues
CREATE issue:affordability CONTENT {
  name: "affordability",
  description: "Housing cost, rent pressure, home prices, and cost-of-living effects."
};

CREATE issue:transport CONTENT {
  name: "transport",
  description: "Commute time, public transport access, congestion, parking, and street movement."
};

CREATE issue:green_space CONTENT {
  name: "green_space",
  description: "Parks, trees, open space, air quality, and environmental quality."
};

CREATE issue:safety CONTENT {
  name: "safety",
  description: "Street safety, traffic safety, lighting, and perceived neighbourhood security."
};

CREATE issue:local_character CONTENT {
  name: "local_character",
  description: "Neighbourhood identity, high street feel, heritage, and change to local fabric."
};

-- Evidence docs
CREATE evidence_doc:ev1 CONTENT {
  title: "Inner London housing pressure summary",
  source_type: "demo_profile",
  snippet: "High housing pressure tends to increase sensitivity to affordability and tenure security concerns.",
  metadata: { issue: "affordability" }
};

CREATE evidence_doc:ev2 CONTENT {
  title: "Transport dependency summary",
  source_type: "demo_profile",
  snippet: "Areas with strong commuter dependency are more sensitive to disruption, travel time, and station access.",
  metadata: { issue: "transport" }
};

CREATE evidence_doc:ev3 CONTENT {
  title: "Green space trade-off summary",
  source_type: "demo_profile",
  snippet: "Residents often weigh new development against impacts on greenery, open space, and environmental quality.",
  metadata: { issue: "green_space" }
};

CREATE evidence_doc:ev4 CONTENT {
  title: "Neighbourhood safety summary",
  source_type: "demo_profile",
  snippet: "Street design, lighting, traffic patterns, and footfall can affect safety perceptions across age groups.",
  metadata: { issue: "safety" }
};

CREATE evidence_doc:ev5 CONTENT {
  title: "Local character summary",
  source_type: "demo_profile",
  snippet: "Support can fall when proposals are seen as weakening neighbourhood identity or displacing existing use.",
  metadata: { issue: "local_character" }
};

-- Segment -> issue edges
RELATE segment:young_renters->CARES_ABOUT->issue:affordability CONTENT { weight: 0.9 };
RELATE segment:young_renters->CARES_ABOUT->issue:transport CONTENT { weight: 0.8 };
RELATE segment:young_renters->CARES_ABOUT->issue:safety CONTENT { weight: 0.6 };

RELATE segment:family_renters->CARES_ABOUT->issue:affordability CONTENT { weight: 0.9 };
RELATE segment:family_renters->CARES_ABOUT->issue:green_space CONTENT { weight: 0.7 };
RELATE segment:family_renters->CARES_ABOUT->issue:safety CONTENT { weight: 0.8 };

RELATE segment:homeowners->CARES_ABOUT->issue:local_character CONTENT { weight: 0.8 };
RELATE segment:homeowners->CARES_ABOUT->issue:safety CONTENT { weight: 0.7 };
RELATE segment:homeowners->CARES_ABOUT->issue:green_space CONTENT { weight: 0.6 };

RELATE segment:commuters->CARES_ABOUT->issue:transport CONTENT { weight: 0.95 };
RELATE segment:commuters->CARES_ABOUT->issue:affordability CONTENT { weight: 0.5 };

RELATE segment:older_residents->CARES_ABOUT->issue:safety CONTENT { weight: 0.8 };
RELATE segment:older_residents->CARES_ABOUT->issue:local_character CONTENT { weight: 0.7 };
RELATE segment:older_residents->CARES_ABOUT->issue:green_space CONTENT { weight: 0.6 };

RELATE segment:local_business_workers->CARES_ABOUT->issue:transport CONTENT { weight: 0.7 };
RELATE segment:local_business_workers->CARES_ABOUT->issue:affordability CONTENT { weight: 0.6 };
RELATE segment:local_business_workers->CARES_ABOUT->issue:local_character CONTENT { weight: 0.5 };
