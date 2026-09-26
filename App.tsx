import { useEffect, useState, type CSSProperties } from "react";

type Team = {
  name: string;
  hp: number;
  maxHp: number;
  inventory: string[];
};

const rounds = [200, 400, 600, 800, 1000, 1500];
const categories = [
  "Cursed Quotes",
  "Pee Pee Poo Poo Hard",
  "I Can't Read",
  "Where Is Zoro?",
  "Where Are The Pixels?",
  "Truck-kun's Hitlist",
  "Inumaki's Playlist",
  "Japanese Culture",
];

const categoryAccents = [
  "#B5542A",
  "#4B7F52",
  "#3E5468",
  "#5A3E6B",
  "#8A5A2E",
  "#B5542A",
  "#4B7F52",
  "#3E5468",
];

const categoryQuestions: Record<string, string> = {
  "I Can't Read":
    "After airing in 2019, a clip from the ending of a famous anime went viral, with fans all over the world copying the actions of the character and posting their own videos. The clip used rotoscoping to make the movement unusually realistic. Considering the amount of movement involved, what am I talking about?",
  "Cursed Quotes":
    "Identify the character who spoke this forbidden line, and name the conflict that immediately followed.",
  "Pee Pee Poo Poo Hard":
    "This cursed technique looks absurd at first glance, but its rules make it one of the most dangerous abilities in its world. Name the technique and its user.",
  "Where Is Zoro?":
    "This swordsman has wandered into the wrong series again. Name the location he intended to reach and the island where he actually arrived.",
  "Where Are The Pixels?":
    "Study the fragmented image and identify the anime, character, and scene before the veil closes.",
  "Truck-kun's Hitlist":
    "Name the protagonist whose ordinary life ended with an unfortunate encounter, beginning their journey into another world.",
  "Inumaki's Playlist":
    "Identify the anime opening or ending from its translated lyric, then name the artist who performed it.",
  "Japanese Culture":
    "Name the Japanese custom being described and explain the meaning it carries in its original context.",
};

type SelectedQuestion = {
  category: string;
  hp: number;
  key: string;
  accent: string;
};

const initialTeams: Team[] = [
  { name: "Team One", hp: 4000, maxHp: 4000, inventory: ["Binding Vow", "Reverse Technique"] },
  { name: "Team Two", hp: 1080, maxHp: 4000, inventory: ["Cursed Tool"] },
  { name: "Team Three", hp: 3260, maxHp: 4000, inventory: ["Veil", "Black Rope"] },
];

function Sigil() {
  return (
    <svg viewBox="0 0 48 48" aria-hidden="true">
      <path d="M24 4 29 16 42 12 34 23 44 32 30 31 28 44 22 33 10 40 15 27 4 20 18 19Z" />
      <circle cx="24" cy="24" r="7" />
      <path d="m20 24 3 3 6-7" />
    </svg>
  );
}

function Chevron({ open }: { open: boolean }) {
  return (
    <svg className={open ? "rotate-90" : ""} viewBox="0 0 20 20" aria-hidden="true">
      <path d="m7 4 6 6-6 6" />
    </svg>
  );
}

function App() {
  const [teams, setTeams] = useState(initialTeams);
  const [amounts, setAmounts] = useState([-200, -200, -200]);
  const [openTeam, setOpenTeam] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState<"board" | "rules">("board");
  const [claimed, setClaimed] = useState<string[]>([]);
  const [deployed, setDeployed] = useState(false);
  const [selectedQuestion, setSelectedQuestion] = useState<SelectedQuestion | null>(null);
  const [answerRevealed, setAnswerRevealed] = useState(false);

  useEffect(() => {
    if (!selectedQuestion) return;
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") setSelectedQuestion(null);
    };
    document.addEventListener("keydown", closeOnEscape);
    return () => document.removeEventListener("keydown", closeOnEscape);
  }, [selectedQuestion]);

  const applyHp = (index: number) => {
    setTeams((current) =>
      current.map((team, teamIndex) =>
        teamIndex === index
          ? { ...team, hp: Math.max(0, Math.min(team.maxHp, team.hp + amounts[index])) }
          : team,
      ),
    );
  };

  const toggleClaim = (key: string) => {
    setClaimed((current) =>
      current.includes(key) ? current.filter((item) => item !== key) : [...current, key],
    );
  };

  const openQuestion = (category: string, hp: number, key: string, accent: string) => {
    setAnswerRevealed(false);
    setSelectedQuestion({ category, hp, key, accent });
  };

  const completeQuestion = () => {
    if (!selectedQuestion) return;
    if (!claimed.includes(selectedQuestion.key)) toggleClaim(selectedQuestion.key);
    setSelectedQuestion(null);
  };

  return (
    <div className="app-shell">
      <aside className="overseer">
        <div className="brand">
          <span className="brand-sigil">
            <Sigil />
          </span>
          <div>
            <p className="eyebrow">Colony 09</p>
            <h2>Overseer</h2>
          </div>
        </div>

        <p className="sidebar-copy">
          Manage cursed energy, combat damage, and recovery between rounds.
        </p>

        <div className="status-strip">
          <span className="status-pulse" />
          Ritual in progress
          <span className="status-count">03 active</span>
        </div>

        <div className="team-list">
          {teams.map((team, index) => {
            const hpPercent = (team.hp / team.maxHp) * 100;
            const isDanger = hpPercent <= 30;
            return (
              <section className={`team-card ${isDanger ? "is-danger" : ""}`} key={team.name}>
                <div className="team-heading">
                  <div>
                    <span className="team-number">0{index + 1}</span>
                    <h3>{team.name}</h3>
                  </div>
                  <strong>
                    {team.hp.toLocaleString()}
                    <small> / {team.maxHp.toLocaleString()}</small>
                  </strong>
                </div>

                <div className="hp-track" aria-label={`${team.name} health: ${team.hp}`}>
                  <span style={{ width: `${hpPercent}%` }} />
                </div>

                {isDanger && <p className="danger-label">Critical condition</p>}

                <div className="hp-controls">
                  <button
                    className="step-button"
                    aria-label={`Decrease ${team.name} adjustment`}
                    onClick={() =>
                      setAmounts((current) =>
                        current.map((value, i) => (i === index ? value - 100 : value)),
                      )
                    }
                  >
                    −
                  </button>
                  <output className={amounts[index] > 0 ? "healing" : "damage"}>
                    {amounts[index] > 0 ? "+" : ""}
                    {amounts[index]}
                  </output>
                  <button
                    className="step-button"
                    aria-label={`Increase ${team.name} adjustment`}
                    onClick={() =>
                      setAmounts((current) =>
                        current.map((value, i) => (i === index ? value + 100 : value)),
                      )
                    }
                  >
                    +
                  </button>
                  <button className="apply-button" onClick={() => applyHp(index)}>
                    Apply
                  </button>
                </div>

                <button
                  className="inventory-toggle"
                  aria-expanded={openTeam === index}
                  onClick={() => setOpenTeam(openTeam === index ? null : index)}
                >
                  <Chevron open={openTeam === index} />
                  Manage items
                  <span>{team.inventory.length}</span>
                </button>
                {openTeam === index && (
                  <ul className="inventory-list">
                    {team.inventory.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                )}
              </section>
            );
          })}
        </div>
      </aside>

      <main className={activeTab === "rules" ? "rules-view" : undefined}>
        <nav className="top-nav">
          <div className="tabs" aria-label="Dashboard sections">
            <button
              className={activeTab === "board" ? "active" : ""}
              onClick={() => setActiveTab("board")}
            >
              Culling board
            </button>
            <button
              className={activeTab === "rules" ? "active" : ""}
              onClick={() => setActiveTab("rules")}
            >
              Rules of engagement
            </button>
          </div>
          <div className="nav-actions">
            <div className="round-status">
              <span />
              Round 04
            </div>
            <button
              className={deployed ? "deploy-button deployed" : "deploy-button"}
              onClick={() => setDeployed((current) => !current)}
            >
              {deployed ? "Deployed" : "Deploy"}
            </button>
          </div>
        </nav>

        {activeTab === "board" ? (
          <>
            <header className="hero">
              <div className="hero-rule">
                <span />
                <Sigil />
                <span />
              </div>
              <p className="eyebrow">Tokyo No. 1 Colony</p>
              <h1>
                <span>死</span> Culling Game <span>滅</span>
              </h1>
              <p className="subtitle">Survive the rounds · Milan quiz edition</p>
              <div className="threat">
                <span>Threat level</span>
                <i />
                <i />
                <i />
                <i />
                <i className="inactive" />
                <b>Severe</b>
              </div>
            </header>

            <section className="board-section">
              <div className="section-heading">
                <div>
                  <p className="eyebrow">Select a cursed seal</p>
                  <h2>Combat Trials</h2>
                </div>
                <p>
                  <span>{claimed.length}</span> / {categories.length * rounds.length} seals broken
                </p>
              </div>

              <div className="board-scroll">
                <div className="game-board">
                  {categories.map((category, categoryIndex) => (
                    <div className="category" key={category}>
                      <div className="category-title">
                        <span>0{categoryIndex + 1}</span>
                        <h3>{category}</h3>
                      </div>
                      {rounds.map((hp) => {
                        const key = `${category}-${hp}`;
                        const isClaimed = claimed.includes(key);
                        return (
                          <button
                            className={`seal ${isClaimed ? "claimed" : ""}`}
                            key={hp}
                            onClick={() =>
                              openQuestion(category, hp, key, categoryAccents[categoryIndex])
                            }
                            aria-pressed={isClaimed}
                          >
                            <span>{isClaimed ? "Broken" : hp.toLocaleString()}</span>
                            <small>{isClaimed ? "Seal" : "HP"}</small>
                          </button>
                        );
                      })}
                    </div>
                  ))}
                </div>
              </div>
            </section>
          </>
        ) : (
          <section className="rules-panel">
            <p className="eyebrow">Binding vow</p>
            <h1>Rules of Engagement</h1>
            <div className="rules-copy">
              <section>
                <h2>Game Setup</h2>
                <ul>
                  <li>
                    <strong>Teams:</strong> Three colonies, with four to five players per team.
                  </li>
                  <li>
                    <strong>HP:</strong> Each team starts at 4,000 HP. The maximum limit is 4,000 HP.
                  </li>
                  <li>
                    <strong>Questions:</strong> Eight sections, with trials ranging from 200 to 1,500 points.
                  </li>
                  <li>
                    <strong>Victory:</strong> The last surviving team claims the colony.
                  </li>
                </ul>
              </section>

              <section>
                <h2>General Rules</h2>
                <ol>
                  <li>
                    <strong>Buzz-In:</strong> The first team to buzz in earns the first opportunity to answer.
                  </li>
                  <li>
                    <strong>No Team Answers:</strong> Control passes to the next team in the colony order.
                  </li>
                  <li>
                    <strong>Correct Answers:</strong> Deal damage equal to the question&apos;s point value to any opposing team.
                  </li>
                  <li>
                    <strong className="danger-term">Incorrect Answers:</strong> Your team loses HP equal to the question&apos;s point value.
                  </li>
                </ol>
              </section>

              <section>
                <h2>Damage &amp; Combat Mechanics</h2>
                <ol start={5}>
                  <li>
                    <strong className="danger-term">Consecutive Damage Multiplier:</strong> If a team takes damage on consecutive turns, incoming damage is reduced by 0.1× per turn, to a minimum of 0.5×. The multiplier resets to 1.0× after one complete turn without damage.
                  </li>
                  <li>
                    <strong>Player Sacrifice:</strong> If a team does not answer for three consecutive questions, it must sacrifice one player to remain in the game. Sacrificed players may not participate in team discussions.
                  </li>
                  <li>
                    <strong>Healing:</strong> Recovery can never raise a team above its starting maximum of 4,000 HP.
                  </li>
                  <li>
                    <strong className="danger-term">Elimination:</strong> A team reduced to zero HP is removed from the colony. No appeal. No return.
                  </li>
                </ol>
              </section>
            </div>
          </section>
        )}
      </main>

      {selectedQuestion && (
        <div
          className="modal-backdrop"
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) setSelectedQuestion(null);
          }}
        >
          <section
            className="question-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="question-title"
            style={{ "--modal-accent": selectedQuestion.accent } as CSSProperties}
          >
            <button
              className="modal-close"
              aria-label="Close question"
              onClick={() => setSelectedQuestion(null)}
            >
              ×
            </button>
            <p className="modal-label">Question</p>
            <h2 id="question-title">
              <span>{selectedQuestion.category}</span>
              <i />
              <b>{selectedQuestion.hp.toLocaleString()} HP</b>
            </h2>
            <div className="modal-divider" />
            <p className="question-copy">
              {categoryQuestions[selectedQuestion.category]}
            </p>

            {answerRevealed && (
              <div className="answer-panel">
                <span>Answer</span>
                {selectedQuestion.category === "I Can't Read"
                  ? "The Chika dance from Kaguya-sama: Love Is War."
                  : "Answer accepted at the Overseer's discretion."}
              </div>
            )}

            <div className="modal-actions">
              <button
                className="reveal-button"
                onClick={() => setAnswerRevealed((current) => !current)}
              >
                {answerRevealed ? "Conceal Answer" : "Reveal Answer"}
              </button>
              <button className="complete-button" onClick={completeQuestion}>
                <span aria-hidden="true" />
                Mark as Done &amp; Close
              </button>
            </div>
          </section>
        </div>
      )}
    </div>
  );
}

export default App;
