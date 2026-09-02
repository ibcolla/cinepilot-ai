# CinePilot AI Demo Flow

This document describes the recommended presenter flow for the CinePilot AI demo and explains why each step matters in a production setting.

## 1. Dashboard

Start on the Dashboard.

What to point out:
- the dashboard is the operational landing page for production oversight
- it frames the continuity workflow as a quick, high-level monitoring view
- it presents the state of the scene analysis and the agent status

Why it matters:
- production teams need a compact view before drilling into the details of a take
- the dashboard communicates the idea that continuity review is part of an ongoing monitoring workflow, not a one-off artifact

## 2. Scene 12

Navigate to the Scene 12 view.

What to point out:
- the scene is a real, tangible example of a production continuity review
- the context is explicit: this is an office-arrival sequence with an approved standard to compare against
- the scene information sets up the expected continuity rules the take should follow

Why it matters:
- production continuity issues are always tied to concrete scene context
- the presenter should emphasize that the system is not guessing; it is comparing a current take against a known production standard

## 3. Analyze Current Take / Live Analysis

Use the Analyze Current Take action.

What to point out:
- this is the live analysis step where the current take is evaluated against production continuity expectations
- the system checks for issues such as wardrobe mismatches, missing props, or inconsistent scene details
- the analysis request is sent to the backend and orchestrator layer for evaluation

Why it matters:
- this is the core decision point for the demo
- it demonstrates how a production team can surface continuity concerns before a take becomes a costly problem in post-production

## 4. Continuity

Open the Continuity review page after analysis.

What to point out:
- the detected issues are presented with severity, category, confidence, observed vs. expected behavior, and remediation guidance
- each issue ties directly to a production problem, not a generic AI summary
- the continuity view is where the team can see why a take may need to be rejected or revisited

Why it matters:
- this is where the value of the product becomes clear: the system transforms a raw take into actionable continuity decisions
- it mirrors how production could review and approve or reject a shot before it becomes an expensive downstream issue

## 5. Production Memory

Navigate to Production Memory.

What to point out:
- the approved decision and production rationale are captured in a memory/decision record
- the system reinforces the approved take and the reason it was accepted
- this creates a reusable production record rather than a one-off comment thread

Why it matters:
- production memory matters because continuity decisions must remain traceable
- teams need to know what was approved, why it was approved, and how that decision informs future takes and scenes

## Presenter guidance

For a strong demo, keep the story focused on one simple message:

CinePilot AI helps production teams detect continuity risk early, compare a current take to the approved standard, and preserve the decision trail for future review.

The demo should feel like a production decision workflow, not a generic chatbot experience. The key value is not the fancy UI alone; it is the practical decision support for continuity management.
