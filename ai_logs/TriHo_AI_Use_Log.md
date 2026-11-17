# AI Use Log: Final Project (CFPB Complaint Classification and AI Governance)

**Tri Ho** | INFO 4340

**Tools used:**
- **Claude Code (Opus 5.5)** in VS Code, for the notebook: 11 sessions between Oct 25 and Nov 17, 2026.
- **Claude Chat**, to help generate the presentation slides (Entry 26).

These are separate from the two models the project studies, Sonnet 5.5 (the labeler) and Opus 5.5 (the pilot comparison), which were called through the API from inside the notebook.

**How this log was written:** drafted by Claude Code from the saved session transcripts (my prompts are quoted from them, typos included), its project notes and the git history, then reviewed and edited by me.

**How I worked with the AI:** each step was designed in chat before any code was written, one step at a time, because handing a whole project to AI in one go creates bugs that take longer to fix later. I ran every cell myself, including every paid API call, and the AI committed only when I said so. Alex built his parts (the classifiers, the first governance memo and back-test) as separate notebooks, and I brought them into the main notebook with Claude Code.

---

## Phase 1: Setting up and exploring (Oct 25-27)

## Entry 1: Ground rules and a transparent setup

**What I asked:** "As you working with me througout multiple project, I lean that handing everything to AI in one step incur alot of 'bugs' that can take even longer to troubleshoot toward the back end." I had it read the project requirements first, then walk me through only two cells (setup and load), without reading the large dataset itself.

**What the AI produced:** the setup and load cells, a project folder structure for GitHub, and a SHA-256 fingerprint check on the data file.

**What I changed or decided:**
- I asked why a hash check was needed at all, then asked for it to be transparent: instead of a hard-coded value, the cell shows both fingerprints with a PASS/FAIL line.
- The AI had built part of the setup in a side `.py` file. I asked for the notebook to stand on its own, so a reader never needs a second file open to follow it.
- I chose CSV over Excel for data files, and a local git repository from the start.

## Entry 2: A data dictionary built from evidence, not memory

**What I asked:** to start with the basics: a data dictionary.

**What the AI produced:** a data dictionary written from its own knowledge of the CFPB fields.

**What I changed or decided:** I pushed back: "it is from your 'memory' the part that neither me nor anyone reading the code see. That can be seen as assumptions." The first cells became a profile of the data (dimensions, types, missingness, uniqueness, value counts), so a reader can see where every dictionary entry comes from. I checked the CFPB data-use page myself and confirmed the AI's quotes before they went in. I chose a coded dictionary for the notebook plus an exported copy in the README.

## Entry 3: Setting vocabulary, and the first model ideas

**What I asked:** to brainstorm directions, since "both of us have no idea where to take this project too. We are not new to analytics, just new to how to work with AI and kind of new with text analytic."

**What the AI produced:** possible use cases (routing, relief triage, extraction, summarization).

**What I changed or decided:**
- I set a vocabulary rule: "model" means the whole modeling block (classifier benchmark plus LLM); the language model is "AI" or "LLM".
- My own idea: the 18,577 "I do not know" sub-product complaints as a possible second model. I made Model 1 the standalone main model and kept the second as a back-pocket option.

## Entry 4: Exploring every target, and reading the charts

**What I asked:** to explore all candidate targets, not only the one we would model: "if we have a visualisation or by mean of data epxloration see a pattern of certain complaints tend to get more money settlement. Then without the modeling that can be an answer."

**What the AI produced:** relief rates by product (its suggestion as a candidate target), dot charts with confidence intervals, and a product-mix chart.

**What I changed or decided:**
- I asked how to read each chart (what the intervals show, what the percentage unit is, what the dashed lines mean), then had those explanations written as markdown under each chart for the reader.
- I found the CFPB's 2025 annual report with the official relief definitions and saved it in the project, so the AI could search the local PDF instead of the internet.
- I told the AI to skip chart images when reading the notebook outside chart work, to save tokens.
- I told it to keep governance framing out of the build for now: "My workstyle is 'data driven'... to have you juggling with all that nuance while I need you to be with me building this is very error prone."

## Entry 5: Finding duplicates, and sleeping on it

**What I asked:** whether the repeated narratives also repeat their structured fields.

**What the AI produced:** duplicate groups: 332 repeated texts, small groups that look like one person filing to several companies, and large groups spread across states.

**What I changed or decided:** my hypothesis was templates from paralegals or advocacy groups, which I recorded as unverified. I chose to sleep on the policy before deciding. I also set up the private GitHub repository with only the essential files, leaving out the raw data and the large report.

---

## Phase 2: Target, cleaning and bookkeeping (Nov 3-4)

## Entry 6: Issue as the target, and the duplicate rules

**What I asked:** Issue as the target ("The IDK subproduct will be in our back pocket"); duplicates removed only within the narratives, since only those can be modeled.

**What the AI produced:** exact and normalized duplicate counts, and a "template family" detector.

**What I changed or decided:**
- The redaction marks (XXXX) appear in almost every narrative, so I asked for the text to be normalized before the duplicate check, not after.
- I read the template texts myself and decided to drop the whole family, with a write-up.
- I asked for the duplicate rules to live inside the single cleaning function, not in a separate cell.

## Entry 7: Rejecting "Other", synonym merging and dropping rare classes

**What the AI proposed:** merging rare Issues into "Other", merging look-alike labels, and removing classes with fewer than 30 narratives.

**What I changed or decided:** I rejected all three. The data is one month and "The last big rewording was done in 2023", so look-alike labels are genuinely distinct options. And on rare classes: "Available Issue directly related to Sub-product which in turn depend on Product. If we take out the rare case, that might actually delete the one option that the consumer actually see." All 83 Issues stayed.

## Entry 8: Catching a decision the AI brought back

**What happened:** a markdown draft from the AI said rare classes would be scored as one pooled group.

**What I changed or decided:** "I think you are hallucinating claude code, is the conversation getting too long?" My issue was not that it made a decision, but that "we ruled out not using Pooled class in the model earlier and now you suggesting it again." We replaced it with the sub-group evaluation taught in class that week, which would surface weak classes on its own.

## Entry 9: The bookkeeping pass

**What I asked:** to comb the notebook section by section "so that it read cleaner, easier for an audience like my partner to pick up on or the professor to grade."

**What the AI produced:** proposals per section; a rebuilt, simpler cleaning function; and two data dictionaries (raw and cleaned).

**What I changed or decided:**
- The two-dictionary idea was mine: one for the raw export, one for the cleaned modeling set.
- After asking how to read the product-mix chart, I put it in my own words ("this is actually two pie chart") and had the whole chart reading rewritten, since "if me asking you how to read this chart, that mean my partner would also have a question here too."
- I set a framing rule: the Candidates 2-4 section shows why Issue is the ideal target, without mentioning Sub-product as a second model. If we never build it, there would be mentions to remove one by one; if we do, "it take only one markdown line to re-introduce."
- I moved the read-back of the saved data to the start of Modeling, and chose to push the 25 MB cleaned CSV to GitHub for grading.

---

## Phase 3: Modeling (Nov 10-11)

## Entry 10: Issues that are not on the form's menu

**What the AI produced:** a finding that 423 narratives have an Issue the complaint form does not offer for their Product and Sub-product.

**What I changed or decided:**
- I disagreed at first ("there should not be any 423 off-menu narratives though") and asked for a sample cell so I could see them. After reading the sample and the form PDF, I agreed: these Issues come through the form's credit-report redirect, and the LLM could never pick them from its menu.
- I decided to drop them, and required the notebook to show how they were found, since "our purpose of this project is to not have a human to read all 14k rows."
- I asked for this to be its own section before Clean, not crowded into Clean, and for the form parser to be reused later as the LLM's menu.

## Entry 11: The labeler, and rules on spending

**What I asked:** to build the labeler from my v2 prompt from the Prompt Output and Evaluation test run ("v2 won, you don't have to look for it"), using the batch API, and "don't do background checking code since that would cost money especially with the LLM prompt."

**What the AI produced:** a batch runner that saves every answer and never pays twice for the same request, plus a pilot on 20 training narratives.

**What I changed or decided:** I asked why a pilot was needed before agreeing to it, and asked for its output to be saved with a cost calculation, so the pilot also gave us a cost projection for the full test run.

## Entry 12: Designing the human rating

**What I asked:** the course lets evaluation use rubric scores, so I proposed "a rubric here with kappa agreement between the LLM, me and partner."

**What the AI produced:** a rating design. It recommended more items and a fully blind design.

**What I changed or decided:**
- I scoped it down: "if this project will be used in production, I would lean toward your suggestion and probably even do 100 blind rating items. However, we have to adjust for scope and time constraint here." The 20 items are documented as a proof of concept.
- The semi-blind pick was my idea: raters choose an Issue before seeing the LLM's answer, which still allows a kappa.
- I set the rubric at 4 dimensions with anchors from 0 to 4, and kept it unfrozen until Alex reviewed and revised it.
- I chose Excel sheets with dropdowns and a free-text justification.

## Entry 13: Opus vs. Sonnet

**What I asked:** to run the same 20 pilot narratives through Opus 5.5, with its own on/off switch so neither model's run could trigger the other.

**What the AI produced:** the Opus pilot. Opus matched the consumer's Issue on 13 of 20 and Sonnet on 14, at more than twice the cost.

**What I changed or decided:** I chose Sonnet for the test run on cost-effectiveness, with a short markdown and no extra comparison code: "a human can see the output and make the judgement."

## Entry 14: The test run

**What I asked:** what to store alongside each answer for the governance work later (the model's response details and a thinking summary), and a line printing the run time.

**What the AI produced:** the full test run: 2,950 narratives in 4.3 minutes for \$7.58.

**What I changed or decided:**
- The thinking summary came back empty. I chose to record that in an observation cell rather than pay for another call to confirm why.
- When the AI changed the test-run cell, I stopped it: "don't ask for commit before I get some clarification first, what did you change." I wanted to understand the change before accepting it.

---

## Phase 4: Bringing in Alex's work, and evaluation (Nov 11-14)

## Entry 15: Classifiers A and B

**What I asked:** to bring Alex's classifier, built in his own notebook, into the main notebook as the LLM's benchmark.

**What the AI produced:** Alex's TF-IDF and logistic regression classifier (Classifier A) in the Modeling section, reproducing his 2,950 test predictions exactly; later his menu-limited version (Classifier B), which also matched his file.

**What I changed or decided:** I asked Alex to add Classifier B using the Issue menus already built for the LLM, so the benchmark and the LLM choose from the same options. Classifier B became the main comparison for the LLM, with Classifier A kept as the narrative-only reference.

## Entry 16: Learning the bootstrap, and a standalone Evaluation

**What I asked:** "why do we need the bootstrap for?", and whether it was still needed alongside a sub-group evaluation.

**What the AI produced:** paired bootstrap confidence intervals and McNemar's test for the model comparisons.

**What I changed or decided:**
- The bootstrap was a new concept for me, so I asked for it to be explained until it made sense, rather than accepting it as given.
- Because tuning is slow, I suggested Evaluation read the saved predictions so it can run on its own.
- I asked for the human-rating read-back and the agreement measures (kappa, MDD) to be split into two cells, and for results to be shown as tables.

## Entry 17: Code cleanup and a decision not to build Classifier C

**What I asked:** to move every package import into Set Up, while keeping each section's own settings at the top of that section ("I don't want to Set Up cell to crowded neither").

**What I changed or decided:** we discussed adding Product and Sub-product as classifier features (Classifier C). Since the expected gain was small, I recorded it as future work instead of building it.

---

## Phase 5: Governance (Nov 14-16)

## Entry 18: The accuracy rule

**What I asked:** to base the trigger on the LLM's lead over Classifier B ("If the LLM start to do worse like <5.7 from a free baseline then we should flag it"), and then "can we use within 1 standard deviation of accuracy difference?"

**What the AI produced:** the rule as a threshold in standard deviations, so the cutoff moves with batch size, with a back-test.

**What I changed or decided:**
- The AI framed full-scale volume as out of scope. I pushed back: "If we want to deploy in production, it would read all the complaint that has text in it... by the time we want to make a point on 'what value does AI pipeline or this project bring in real business setting' we will lose that battle there."
- I asked for Alex's first version to be told as a first draft that we improved on, not as a mistake.

## Entry 19: Bias & Fairness: what the metrics are for

**What I asked:** whether the disparate impact ratio made sense here. Alex's ratio flagged almost every Product, but "if we tune up to 2.5, that feels a little more like a convinient move."

**What I changed or decided:**
- The key insight was mine: "these three dimension live in the demographic side of the dataset - something that describe the people... But when these complaint do not share a similar targets (Issue) in our case. It make the application of these metrics feel off." So the Product rule became: accept each Product's measured error level and fire only if it gets worse beyond noise (a tolerance band).
- I asked to check the consumer groups (Older Americans, servicemembers) as the place where fairness metrics do fit. The LLM served both equally.
- I caught the AI's summary claiming a four-fifths rule we had not used in the final rule, and set the principle for section 3: "the final rule is what we applied as rule, not what we rule out."
- When I noticed a batch-size change I had not approved, I had it reverted: "There are many changes to keep track on, so I rather do one change at a time."

## Entry 20: The human review rule

**What I asked:** to combine the disagreement trigger with a cutoff on the LLM's confidence, and for a histogram of confidence on the wrong answers only.

**What the AI produced:** a chart that also showed a second panel I had not asked for.

**What I changed or decided:**
- I corrected it: "you misread me though... I am asking for chart that show the confidence level distribution on the wrong complaint only... I did not say I want one chart that show two things."
- When the AI noted that the chart shows how many answers are wrong, not how often, I asked for the second chart: "I need to see it."
- From the two charts I chose 0.70 as the balance point. I asked for the trade-off against Version 1 (false positives against false negatives) in its own cell.

## Entry 21: The domains we did not back-test

**What I asked:** a markdown cell explaining why three higher-scoring risks (Disclosure, Documentation, Accountability) have no back-test, with qualitative controls instead: staff checklists, a clear AI label for consumers, and a chain of custody with an escalation path.

**What I changed or decided:** my reasoning, which the cell records: writing a numeric trigger for these "require internal working knowledge of how each complaint process", which is beyond the project's scope. I also removed small headings that made text too small and kept them as plain labels.

## Entry 22: The business case and its framing

**What I asked:** to define the business case and question before the qualitative sections, discussing in chat before anything was written.

**What the AI produced:** drafts of the background, motivation and business question.

**What I changed or decided:**
- I removed every mention of "trend summaries": it was "a cross polinating idea" from the CFPB annual report, which builds its trends from the data with no AI.
- I asked how CFPB actually handles a complaint. Learning that it routes by company name, I reframed the benefit: the complaint lands in the right queue on the company's side, not that CFPB routes it better.
- The design was mine: consumers keep choosing Product and Sub-product, and an optional LLM suggests Issues from a more detailed menu; this project is the groundwork for it.
- When the AI asked me to agree to three points at once, I stopped it: "you cannot ask me three things to agree on and then go to Motivation 1."
- The Reflection thesis is mine: the ceiling is closeness to a noisy human judgment, so after a few gains a better model gives diminishing returns, and "the true AI frontier" is a better-defined use case.

## Entry 23: LLM cost and the harm estimate

**What I asked:** a cost cell projecting tokens to a month of complaints, and a harm estimate with two figures: the share of complaints the LLM gets wrong, projected to a full month, and a rework cost based on staff wages.

**What I changed or decided:** I dropped Alex's generic \$15 per misroute. I also ruled out timing the rating exercise as a proxy for review time, because it includes rubric scoring, which a staff reviewer would never do.

---

## Phase 6: Final polish (Nov 17)

## Entry 24: The polish pass

**What I asked:** a final section-by-section tidy-up, with before/after snippets in chat because "it is hard to locate one line of code in such a big notebook", and a log of every change so a top-to-bottom run would show anything broken.

**What the AI produced:** proposals per section, a change log, and checks I could not run myself: every code cell compiles, and the harm-estimate figures recomputed independently from the saved files matched.

**What I changed or decided:** I approved each batch, then ran the whole notebook top to bottom: no errors and no failed checks. The AI pointed out two of its own mistakes: a wrong claim about type hints, and a reordered version line it had said would not change.

## Entry 25: Notebook structure, the test-run summary, and escalation

**What I asked:** a summary of the Prompt Output and Evaluation test run in the labeler section, and a guide at the top of the notebook.

**What I changed or decided:**
- I reshaped the guide from a glossary into a "Notebook Structure" outline that shows the many directions we explored and set aside, plus a list of important features and metrics.
- The AI suggested an independent decision-maker for escalations. I added it, then removed it: "the owner should be the one who implement the rule... the escalation is pretty flag, since noone contracting us, and the complaint resolving process vary per company where CFPB only routing it."

## Entry 26: Claude Chat for the presentation slides

**Tool:** Claude Chat.

**What I asked:** help building the presentation from the finished notebook: extract the key numbers, and re-render code snippets and certain visuals to match the deck's theme.

**What the AI produced:** slides built from the notebook's results, with the selected charts and code restyled for the deck.

**What I changed or decided:** I chose which results and visuals went into the deck, and the numbers come from the notebook's printed outputs.

---

## Reflection

*[to write]*
