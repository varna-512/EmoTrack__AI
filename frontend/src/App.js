import { useState, useEffect, useMemo, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import MicRecorder from "mic-recorder-to-mp3";
import Webcam from "react-webcam";

import {
  Activity,
  BarChart3,
  Bell,
  Brain,
  CalendarDays,
  Camera,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  ClipboardList,
  Download,
  Dumbbell,
  FileText,
  Flame,
  Gauge,
  HeartPulse,
  HelpCircle,
  Home,
  LineChart as LineChartIcon,
  Lock,
  Moon,
  Music,
  Play,
  Search,
  Settings,
  ShieldAlert,
  Sparkles,
  Target,
  User,
  Volume2,
  Waves,
  Wind,
} from "lucide-react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import "./App.css";

const recorder = new MicRecorder({ bitRate: 128 });
const API_BASE = "http://127.0.0.1:8000/api";

const navItems = [
  { id: "dashboard", label: "Dashboard", icon: Home },
  { id: "assessment", label: "Assessment", icon: ClipboardList },
  { id: "results", label: "Results & Recommendations", icon: Brain },
  { id: "insights", label: "Insights & Progress", icon: BarChart3 },
  { id: "reports", label: "Reports History", icon: FileText },
  { id: "goals", label: "Wellness Goals", icon: Target },
  { id: "profile", label: "Profile", icon: User },
  { id: "settings", label: "Settings", icon: Settings },
  { id: "help", label: "Help & Support", icon: HelpCircle },
];

const steps = [
  "Pulse Monitoring",
  "Face Analysis",
  "Voice Analysis",
  "Text Analysis",
  "AI Processing",
  "Results",
  "Recommendations",
];

const recommendations = [
  { icon: Wind, title: "Mindfulness", description: "Three-minute grounding routine with breath pacing.", cta: "Begin" },
  { icon: Brain, title: "Meditation", description: "Guided session tuned for post-assessment regulation.", cta: "Open" },
  { icon: Music, title: "Music", description: "Low-tempo soundscape for recovery and focus.", cta: "Play" },
  { icon: Dumbbell, title: "Exercise", description: "Light mobility sequence to reduce physical tension.", cta: "Start" },
  { icon: Moon, title: "Sleep", description: "Evening wind-down checklist and sleep consistency goal.", cta: "Plan" },
  { icon: Gauge, title: "Stress Management", description: "Identify triggers and choose a coping protocol.", cta: "Review" },
  { icon: HeartPulse, title: "Social Wellness", description: "Nudge to connect with a trusted support person.", cta: "Schedule" },
];

const prompts = [
  "What emotion has been most present today?",
  "What felt heavy, and what felt supportive?",
  "Describe one moment you want the AI to understand.",
];

function getFinalResult(result) {
  return result?.final_result || {};
}

function percent(value, fallback = 0) {
  const numeric = Number(value);
  if (Number.isFinite(numeric)) {
    const scaled = numeric <= 1 ? numeric * 100 : numeric;
    return Math.max(0, Math.min(100, Math.round(scaled)));
  }
  return fallback;
}

function emotionDistributionFromResult(finalResult, dashboardData) {
  const probabilities = finalResult?.final_probabilities || {};
  const colors = ["#14b8a6", "#6366f1", "#f97316", "#64748b", "#22c55e", "#ef4444"];
  const distribution = Object.entries(probabilities).map(([name, value], index) => ({
    name,
    value: percent(value),
    color: colors[index % colors.length],
  }));

  return distribution.length ? distribution : dashboardData?.emotion_distribution || [];
}

function modalityScoresFromResult(faceResult, voiceResult, finalResult, dashboardData) {
  if (faceResult?.confidence || voiceResult?.confidence || finalResult?.confidence) {
    return [
      { metric: "Face", score: percent(faceResult?.confidence) },
      { metric: "Voice", score: percent(voiceResult?.confidence) },
      { metric: "Fusion", score: percent(finalResult?.confidence) },
    ];
  }

  return dashboardData?.modality_scores || [];
}

function App() {
  const [activeView, setActiveView] = useState("dashboard");
  const [collapsed, setCollapsed] = useState(false);
  const [darkMode, setDarkMode] = useState(true);
  const [step, setStep] = useState(0);
  const [isRecording, setIsRecording] = useState(false);
  const [loading, setLoading] = useState(false);
  const [cameraOn, setCameraOn] = useState(false);
  const [result, setResult] = useState(null);
  const [audioFile, setAudioFile] = useState(null);
  const [audioUrl, setAudioUrl] = useState("");
  const [imageFile, setImageFile] = useState(null);
  const [journal, setJournal] = useState("");
  const [typingStartTime, setTypingStartTime] = useState(null);
  const [typingSpeed, setTypingSpeed] = useState(0);
  const [textEmotion, setTextEmotion] = useState("");
  const [textTrigger, setTextTrigger] = useState("");
  const [textIntensity, setTextIntensity] = useState(5);
  const [textDuration, setTextDuration] = useState("");
  
  const [pulse, setPulse] = useState(76);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortKey, setSortKey] = useState("date");
  const [filterStatus, setFilterStatus] = useState("All");
  
  const [history, setHistory] = useState([]);
  const [dashboardData, setDashboardData] = useState(null);
  const loadDatabaseData = useCallback(async ({ useLatestResult = false } = {}) => {
    const [historyResponse, dashboardResponse] = await Promise.all([
      fetch(`${API_BASE}/history/`),
      fetch(`${API_BASE}/dashboard/`),
    ]);
    const [historyData, dashboard] = await Promise.all([
      historyResponse.json(),
      dashboardResponse.json(),
    ]);

    setHistory(Array.isArray(historyData) ? historyData : []);
    setDashboardData(dashboard);

    if (useLatestResult) {
      const latestResult = dashboard?.latest_result || historyData?.[0]?.result || null;
      setResult(latestResult);
    }
  }, []);
  useEffect(() => {

  fetch("http://127.0.0.1:8000/api/history/")
    .then((res) => res.json())
    .then((data) => {

      console.log("History API:", data);

      setHistory(data);

    })
    .catch((err) => {

      console.error(err);

    });

}, []);

  useEffect(() => {
    loadDatabaseData({ useLatestResult: true }).catch(console.error);
  }, [loadDatabaseData]);
  const reports = history.map((item) => ({

  date: new Date(item.date)
    .toLocaleDateString(),

  emotion: item.final_emotion,

  wellness: Math.round(
    item.confidence * 100
  ),

  stress: item.stress_score,

  status: "Complete"
}));
  const webcamRef = useRef(null);
  const finalResult = getFinalResult(result);
  const voiceResult = result?.voice_result || {};
  const faceResult = result?.face_result || {};
  const primaryEmotion = finalResult.final_emotion || dashboardData?.latest_emotion || "N/A";
  const confidence = percent(finalResult.confidence ?? dashboardData?.latest_confidence);
  const stressScore = percent(finalResult.stress_score ?? dashboardData?.latest_stress);
  const trendData = dashboardData?.trend_data || [];
  const emotionDistribution = emotionDistributionFromResult(finalResult, dashboardData);
  const modalityScores = modalityScoresFromResult(faceResult, voiceResult, finalResult, dashboardData);
  const wellnessMetrics = dashboardData?.wellness_metrics || [];

  const filteredReports = useMemo(() => {
    return reports
      .filter((report) => {
        const matchesSearch = `${report.date} ${report.emotion} ${report.status}`
          .toLowerCase()
          .includes(searchTerm.toLowerCase());
        const matchesStatus = filterStatus === "All" || report.status === filterStatus;
        return matchesSearch && matchesStatus;
      })
      .sort((a, b) => {
        if (sortKey === "wellness") return b.wellness - a.wellness;
        if (sortKey === "stress") return b.stress - a.stress;
        return new Date(b.rawDate) - new Date(a.rawDate);
      });
  }, [filterStatus, reports, searchTerm, sortKey]);

  const startRecording = async () => {
    try {
      await recorder.start();
      setIsRecording(true);
    } catch (error) {
      console.log(error);
    }
  };

  const stopRecording = async () => {
    try {
      setLoading(true);
      const [, blob] = await recorder.stop().getMp3();
      setIsRecording(false);
      const file = new File([blob], "voice.wav", { type: "audio/wav" });
      setAudioFile(file);
      setAudioUrl(URL.createObjectURL(blob));
      setLoading(false);
    } catch (error) {
      console.log(error);
      setLoading(false);
    }
  };

  const captureFace = async () => {
    try {
      const imageSrc = webcamRef.current.getScreenshot();
      const blob = await fetch(imageSrc).then((res) => res.blob());
      const file = new File([blob], "face.jpg", { type: "image/jpeg" });
      setImageFile(file);
    } catch (error) {
      console.log(error);
    }
  };

  const analyzeEmotion = async () => {
    try {
      setLoading(true);
      const formData = new FormData();

      if (audioFile) {
        formData.append("audio", audioFile);
      }

      if (imageFile) {
        formData.append("image", imageFile);
      }
const assessmentText = `
Primary Emotion: ${textEmotion}
Trigger: ${textTrigger}
Intensity: ${textIntensity}/10
Duration: ${textDuration}
Typing Speed: ${typingSpeed} WPM

Journal:
${journal}
`;

      formData.append("text", assessmentText);

      console.log("TEXT SENT:");
      console.log(assessmentText);
      const response = await fetch(`${API_BASE}/multimodal/predict/`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log(data)
      console.log("VOICE", data.voice_result);
      console.log("FACE", data.face_result);
      console.log("TEXT EMOTION:", textEmotion);
      console.log("TEXT TRIGGER:", textTrigger);
      console.log("TEXT INTENSITY:", textIntensity);
      console.log("TEXT DURATION:", textDuration);
      console.log("JOURNAL:", journal);      
      console.log("FINAL", data.final_result);
      setResult(data);
      await loadDatabaseData();
      setLoading(false);
      setStep(5);
      setActiveView("results");
    } catch (error) {
      console.log(error);
      setLoading(false);
    }
  };

  const navigateTo = (view) => {
    setActiveView(view);
    if (view === "assessment") {
      setStep(0);
    }
  };

  const goToStep = (nextStep) => {
    setStep(Math.max(0, Math.min(steps.length - 1, nextStep)));
  };

  return (
    <div className={darkMode ? "app dark" : "app"}>
      <Sidebar
        activeView={activeView}
        collapsed={collapsed}
        onCollapse={() => setCollapsed((value) => !value)}
        onNavigate={navigateTo}
      />

      <main className={collapsed ? "main collapsed" : "main"}>
        <Topbar darkMode={darkMode} setDarkMode={setDarkMode} />

        <AnimatePresence mode="wait">
          <motion.section
            key={activeView}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ duration: 0.25 }}
            className="view"
          >
            {activeView === "dashboard" && (
              <Dashboard
              dashboardData={dashboardData}
              primaryEmotion={primaryEmotion}
              confidence={confidence}
              stressScore={stressScore}
              trendData={trendData}
              emotionDistribution={emotionDistribution}
              onNavigate={navigateTo}
             />
            )}
            {activeView === "assessment" && (
              <Assessment
                step={step}
                setStep={goToStep}
                typingStartTime={typingStartTime}
                setTypingStartTime={setTypingStartTime}
                typingSpeed={typingSpeed}
                setTypingSpeed={setTypingSpeed}
                isRecording={isRecording}
                loading={loading}
                cameraOn={cameraOn}
                setCameraOn={setCameraOn}
                webcamRef={webcamRef}
                captureFace={captureFace}
                imageFile={imageFile}
                startRecording={startRecording}
                stopRecording={stopRecording}
                audioFile={audioFile}
                audioUrl={audioUrl}
                journal={journal}
                setJournal={setJournal}
                textEmotion={textEmotion}
                setTextEmotion={setTextEmotion}

                textTrigger={textTrigger}
                setTextTrigger={setTextTrigger}

                textIntensity={textIntensity}
                setTextIntensity={setTextIntensity}

                textDuration={textDuration}
                setTextDuration={setTextDuration}
                analyzeEmotion={analyzeEmotion}
                pulse={pulse}
                setPulse={setPulse}
                result={result}
                finalResult={finalResult}
                confidence={confidence}
                stressScore={stressScore}
                faceResult={faceResult}
                voiceResult={voiceResult}
                dashboardData={dashboardData}
                emotionDistribution={emotionDistribution}
                modalityScores={modalityScores}
                wellnessMetrics={wellnessMetrics}
              />
            )}
            {activeView === "results" && (
              <ResultsAndRecommendations
                result={result}
                finalResult={finalResult}
                confidence={confidence}
                stressScore={stressScore}
                faceResult={faceResult}
                voiceResult={voiceResult}
                dashboardData={dashboardData}
                emotionDistribution={emotionDistribution}
                modalityScores={modalityScores}
                wellnessMetrics={wellnessMetrics}
              />
            )}
            {activeView === "insights" && (
              <Insights
                trendData={trendData}
                emotionDistribution={emotionDistribution}
              />
            )}
            {activeView === "reports" && (
              <Reports
                reports={filteredReports}
                searchTerm={searchTerm}
                setSearchTerm={setSearchTerm}
                sortKey={sortKey}
                setSortKey={setSortKey}
                filterStatus={filterStatus}
                setFilterStatus={setFilterStatus}
              />
            )}
            {activeView === "goals" && <Goals />}
            {activeView === "profile" && <Profile />}
            {activeView === "settings" && <SettingsView />}
            {activeView === "help" && <Help />}
          </motion.section>
        </AnimatePresence>
      </main>

      <AssistantWidget />
    </div>
  );
}

function Sidebar({ activeView, collapsed, onCollapse, onNavigate }) {
  return (
    <aside className={collapsed ? "sidebar collapsed" : "sidebar"}>
      <div className="brand">
        <div className="brand-mark">
          <Sparkles size={20} />
        </div>
        {!collapsed && (
          <div>
            <strong>EmoTrack AI</strong>
            <span>Clinical wellness intelligence</span>
          </div>
        )}
      </div>

      <button className="collapse-button" onClick={onCollapse} aria-label="Toggle sidebar">
        {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
      </button>

      <nav className="nav-list">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              className={activeView === item.id ? "nav-item active" : "nav-item"}
              onClick={() => onNavigate(item.id)}
              title={collapsed ? item.label : undefined}
            >
              <Icon size={19} />
              {!collapsed && <span>{item.label}</span>}
            </button>
          );
        })}
      </nav>
    </aside>
  );
}

function Topbar({ darkMode, setDarkMode }) {
  return (
    <header className="topbar">
      <div>
        {new Date().toLocaleDateString("en-US", {
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric",
          })}
        <h1>EmoTrack AI</h1>
      </div>
      <div className="topbar-actions">
        <button className="icon-button" aria-label="Notifications">
          <Bell size={18} />
        </button>
        <button className="mode-toggle" onClick={() => setDarkMode((value) => !value)}>
          {darkMode ? <Moon size={17} /> : <Sparkles size={17} />}
          <span>{darkMode ? "Dark" : "Light"}</span>
        </button>
      </div>
    </header>
  );
}

function Dashboard({

  dashboardData,

  primaryEmotion,

  confidence,

  stressScore,

  trendData,

  emotionDistribution,

  onNavigate
}) {
  const kpis = [

  {
    label: "Wellness Score",

    value: dashboardData?.wellness_score || 0,

    suffix: "/100",

    icon: HeartPulse,

    tone: "teal"
  },

  {
    label: "Stress Score",

    value:
      dashboardData?.latest_stress || 0,

    suffix: "/100",

    icon: Gauge,

    tone: "orange"
  },

  {
    label: "Emotional Stability",

    value:
      dashboardData?.emotional_stability || 0,

    suffix: "%",

    icon: Activity,

    tone: "indigo"
  },

  {
    label: "Mood Trend",

    value:
      dashboardData?.latest_emotion || "N/A",

    suffix: "",

    icon: LineChartIcon,

    tone: "green"
  },

  {
    label:
      "Assessments Completed",

    value:
      dashboardData?.total_assessments || 0,

    suffix: "",

    icon: CheckCircle2,

    tone: "slate"
  }

];

  return (
    <div className="stack">
      <section className="welcome-band">
        <div>
          <p className="eyebrow">Welcome back, Alex</p>
          <h2>Your emotional status is {primaryEmotion === "N/A" ? "not available yet" : primaryEmotion.toLowerCase()}</h2>
          <p>
            {dashboardData?.total_assessments
              ? `Last assessment showed ${confidence}% confidence with a ${stressScore}/100 stress score.`
              : "Run an assessment to build your database-backed dashboard."}
          </p>
        </div>
        <div className="status-orbit">
          <HeartPulse size={32} />
          <strong>{primaryEmotion}</strong>
          <span>Latest AI readout</span>
        </div>
      </section>

      <section className="kpi-grid">
        {kpis.map((kpi) => (
          <MetricCard key={kpi.label} {...kpi} />
        ))}
      </section>

      <section className="dashboard-grid">
        <div className="panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Quick actions</p>
              <h3>Continue care workflow</h3>
            </div>
          </div>
          <div className="action-grid">
            <button className="primary-action" onClick={() => onNavigate("assessment")}>
              <Play size={18} />
              Start Assessment
            </button>
            <button className="secondary-action" onClick={() => onNavigate("results")}>
              <FileText size={18} />
              View Latest Report
            </button>
            <button className="secondary-action" onClick={() => onNavigate("insights")}>
              <BarChart3 size={18} />
              View Insights
            </button>
          </div>
        </div>

        <div className="panel ai-summary">
          <p className="eyebrow">AI wellness summary</p>
          <h3>{dashboardData?.latest_emotion || "No saved readout yet"}</h3>
          <p>
            {dashboardData?.total_assessments
              ? `Database average stress is ${dashboardData.average_stress}/100 across ${dashboardData.total_assessments} saved assessment${dashboardData.total_assessments === 1 ? "" : "s"}.`
              : "Complete an assessment to populate this summary from stored results."}
          </p>
        </div>
      </section>

      <section className="analytics-grid">
        <ChartPanel title="Mood Trends">
          <ResponsiveContainer width="100%" height={220}>
            <AreaChart data={trendData}>
              <defs>
                <linearGradient id="mood" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#14b8a6" stopOpacity={0.45} />
                  <stop offset="95%" stopColor="#14b8a6" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="day" />
              <YAxis hide />
              <Tooltip />
              <Area type="monotone" dataKey="mood" stroke="#14b8a6" fill="url(#mood)" strokeWidth={3} />
            </AreaChart>
          </ResponsiveContainer>
        </ChartPanel>
        <ChartPanel title="Stress Trends">
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="day" />
              <YAxis hide />
              <Tooltip />
              <Line type="monotone" dataKey="stress" stroke="#f97316" strokeWidth={3} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </ChartPanel>
        <ChartPanel title="Emotion Distribution">
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie data={emotionDistribution} dataKey="value" innerRadius={54} outerRadius={82} paddingAngle={4}>
                {emotionDistribution.map((entry) => (
                  <Cell key={entry.name} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </ChartPanel>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">Recent activity</p>
            <h3>Care timeline</h3>
          </div>
        </div>
        <div className="timeline">
          {(dashboardData?.recent_activity || []).map((item, index) => (
            <div className="timeline-item" key={`${item.label}-${item.time}`}>
              <span>{index + 1}</span>
              <div>
                <strong>{item.label}</strong>
                <p>{item.time}</p>
              </div>
            </div>
          ))}
          {!dashboardData?.recent_activity?.length && <p className="muted">No assessments saved yet.</p>}
        </div>
      </section>
    </div>
  );
}

function MetricCard({ label, value, suffix, icon: Icon, tone }) {
  return (
    <motion.article className={`metric-card ${tone}`} whileHover={{ y: -4 }}>
      <div className="metric-icon">
        <Icon size={20} />
      </div>
      <span>{label}</span>
      <strong>
        {value}
        <small>{suffix}</small>
      </strong>
    </motion.article>
  );
}

function Assessment(props) {
  const {
    step,
    setStep,
    isRecording,
    loading,
    cameraOn,
    setCameraOn,
    webcamRef,
    captureFace,
    imageFile,
    startRecording,
    stopRecording,
    audioFile,
    audioUrl,
    journal,
    setJournal,
    textEmotion,
    setTextEmotion,

    textTrigger,
    setTextTrigger,

    textIntensity,
    setTextIntensity,

    textDuration,
    setTextDuration,
    analyzeEmotion,
    pulse,
    setPulse,
    finalResult,
    stressScore,
    confidence,
    faceResult,
    voiceResult,
    dashboardData,
    emotionDistribution,
    modalityScores,
    wellnessMetrics,
    typingStartTime,
    setTypingStartTime,
    typingSpeed,
    setTypingSpeed,
  } = props;

  return (
    <div className="assessment-layout">
      <ProgressTracker step={step} setStep={setStep} />
      <section className="assessment-stage">
        {step === 0 && <PulseStep pulse={pulse} setPulse={setPulse} onNext={() => setStep(1)} />}
        {step === 1 && (
          <FaceStep
            cameraOn={cameraOn}
            setCameraOn={setCameraOn}
            webcamRef={webcamRef}
            captureFace={captureFace}
            imageFile={imageFile}
            onNext={() => setStep(2)}
            faceResult={faceResult}
          />
        )}
        {step === 2 && (
          <VoiceStep
            isRecording={isRecording}
            loading={loading}
            startRecording={startRecording}
            stopRecording={stopRecording}
            audioFile={audioFile}
            audioUrl={audioUrl}
            onNext={() => setStep(3)}
          />
        )}
        {step === 3 && <TextStep
          textEmotion={textEmotion}
          setTextEmotion={setTextEmotion}

          textTrigger={textTrigger}
          setTextTrigger={setTextTrigger}

          textIntensity={textIntensity}
          setTextIntensity={setTextIntensity}

          textDuration={textDuration}
          setTextDuration={setTextDuration}

          journal={journal}
          setJournal={setJournal}
          typingStartTime={typingStartTime}
          setTypingStartTime={setTypingStartTime}
          typingSpeed={typingSpeed}
          setTypingSpeed={setTypingSpeed}

          onNext={() => setStep(4)}
        /> }
        {step === 4 && <ProcessingStep loading={loading} analyzeEmotion={analyzeEmotion} />}
        {step === 5 && (<ResultReport
        finalResult={finalResult}
       confidence={confidence}
       stressScore={stressScore}
      faceResult={faceResult}
      voiceResult={voiceResult}
      dashboardData={dashboardData}
      emotionDistribution={emotionDistribution}
      modalityScores={modalityScores}
      wellnessMetrics={wellnessMetrics}
      />
      )}
        {step === 6 && <RecommendationGrid />}
      </section>
    </div>
  );
}

function ProgressTracker({ step, setStep }) {
  return (
    <div className="progress-tracker">
      {steps.map((label, index) => (
        <button key={label} className={index <= step ? "step-pill active" : "step-pill"} onClick={() => setStep(index)}>
          <span>{index + 1}</span>
          <strong>{label}</strong>
        </button>
      ))}
    </div>
  );
}

function PulseStep({ pulse, setPulse, onNext }) {
  const pulseData = useMemo(
    () => Array.from({ length: 18 }, (_, index) => ({ label: index, value: pulse + Math.sin(index) * 8 })),
    [pulse]
  );

  return (
    <div className="step-grid">
      <div className="hero-panel">
        <p className="eyebrow">Step 1</p>
        <h2>Pulse Monitoring</h2>
        <p>Capture a quick baseline before the multimodal AI assessment begins.</p>
        <div className="heart-animation">
          <HeartPulse size={42} />
        </div>
      </div>
      <div className="panel">
        <div className="heart-card">
          <span>Heart Rate</span>
          <strong>{pulse} BPM</strong>
          <input type="range" min="58" max="112" value={pulse} onChange={(event) => setPulse(event.target.value)} />
        </div>
        <ResponsiveContainer width="100%" height={220}>
          <LineChart data={pulseData}>
            <XAxis dataKey="label" hide />
            <YAxis hide />
            <Tooltip />
            <Line dataKey="value" stroke="#ef4444" strokeWidth={3} dot={false} />
          </LineChart>
        </ResponsiveContainer>
        <button className="primary-action full" onClick={onNext}>
          Continue
        </button>
      </div>
    </div>
  );
}

function FaceStep({
 cameraOn,
 setCameraOn,
 webcamRef,
 captureFace,
 imageFile,
 onNext,
 faceResult
}){
  return (
    <div className="step-grid">
      <div className="panel camera-panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">Step 2</p>
            <h2>Face Analysis</h2>
          </div>
          <Camera size={22} />
        </div>
        {!cameraOn && (
          <button className="primary-action" onClick={() => setCameraOn(true)}>
            <Camera size={18} />
            Start Camera
          </button>
        )}
        {cameraOn && (
          <div className="camera-frame">
            <Webcam audio={false} ref={webcamRef} mirrored={true} screenshotFormat="image/jpeg" className="webcam" />
            <div className="face-overlay" />
          </div>
        )}
        <div className="button-row">
          <button className="secondary-action" onClick={captureFace} disabled={!cameraOn}>
            Capture
          </button>
          <button className="secondary-action" onClick={() => setCameraOn(false)}>
            Retake
          </button>
          <button className="primary-action" onClick={onNext} disabled={!imageFile}>
            Continue
          </button>
        </div>
      </div>
      <ProbabilityBars faceResult={faceResult} />
    </div>
  );
}

function ProbabilityBars({ faceResult }) {

  const probs =
    faceResult?.emotion_probs || {};

  return (
    <div className="panel">

      <p className="eyebrow">
        Emotion probabilities
      </p>

      <h3>
        Face Model Output
      </h3>

      <div className="bars">

        {Object.entries(probs).map(
          ([emotion, score]) => (

            <div
              className="bar-row"
              key={emotion}
            >

              <span>{emotion}</span>

              <div>
                <i
                  style={{
                    width: `${score * 100}%`
                  }}
                />
              </div>

              <strong>
                {Math.round(score * 100)}%
              </strong>

            </div>

          )
        )}

      </div>

    </div>
  );
}


function VoiceStep({ isRecording, loading, startRecording, stopRecording, audioFile, audioUrl, onNext }) {
  return (
    <div className="step-grid">
      <div className="hero-panel center">
        <p className="eyebrow">Step 3</p>
        <h2>Voice Analysis</h2>
        <button className={isRecording ? "mic-button recording" : "mic-button"} onClick={isRecording ? stopRecording : startRecording}>
          <Volume2 size={34} />
        </button>
        <strong className="timer">{isRecording ? "Recording..." : loading ? "Saving..." : "00:30 sample"}</strong>
        <div className="waveform">
          {Array.from({ length: 28 }, (_, index) => (
            <span key={index} style={{ height: `${18 + ((index * 7) % 44)}px` }} />
          ))}
        </div>
      </div>
      <div className="panel">
        <p className="eyebrow">Playback preview</p>
        <h3>{audioFile ? "Voice sample ready" : "No recording yet"}</h3>
        {audioUrl ? <audio controls src={audioUrl} className="audio-player" /> : <p className="muted">Record a short voice sample to enable playback.</p>}
        <button className="primary-action full" onClick={onNext} disabled={!audioFile}>
          Continue
        </button>
      </div>
    </div>
  );
}

function TextStep({
  textEmotion,
  setTextEmotion,

  textTrigger,
  setTextTrigger,

  textIntensity,
  setTextIntensity,

  textDuration,
  setTextDuration,

  journal,
 setJournal,

typingStartTime,
setTypingStartTime,
typingSpeed,
setTypingSpeed,

onNext
}) {

  const handleTyping = (e) => {
    const text = e.target.value;

    if (!typingStartTime) {
      setTypingStartTime(Date.now());
    }

    setJournal(text);

    const elapsed =
      (Date.now() - (typingStartTime || Date.now())) /
      60000;

    const words = text.trim().split(/\s+/).length;

    if (elapsed > 0) {
      setTypingSpeed(
        Math.round(words / elapsed)
      );
    }
  };

  return ( <div className="step-grid"> <div className="panel text-panel">


      <p className="eyebrow">Step 4</p>

      <h2>AI Emotional Check-In</h2>

      <div className="question-block">
        <label>Primary Emotion</label>

        <select
          value={textEmotion}
          onChange={(e) =>
            setTextEmotion(e.target.value)
          }
        >
          <option value="">
            Select Emotion
          </option>

          <option value="happy">
            Happy
          </option>

          <option value="sad">
            Sad
          </option>

          <option value="angry">
            Angry
          </option>

          <option value="anxious">
            Anxious
          </option>

          <option value="neutral">
            Neutral
          </option>

          <option value="exhausted">
            Exhausted
          </option>

          <option value="frustrated">
            Frustrated
          </option>
        </select>
      </div>

      <div className="question-block">
        <label>
          What influenced this feeling most?
        </label>

        <select
          value={textTrigger}
          onChange={(e) =>
            setTextTrigger(e.target.value)
          }
        >
          <option value="">
            Select Trigger
          </option>

          <option value="Studies">
            Studies
          </option>

          <option value="Work">
            Work
          </option>

          <option value="Relationships">
            Relationships
          </option>

          <option value="Family">
            Family
          </option>

          <option value="Health">
            Health
          </option>

          <option value="Finances">
            Finances
          </option>

          <option value="Other">
            Other
          </option>
        </select>
      </div>

      <div className="question-block">
        <label>
          How intense is this feeling?
        </label>

        <input
          type="range"
          min="1"
          max="10"
          value={textIntensity}
          onChange={(e) =>
            setTextIntensity(e.target.value)
          }
        />

        <span className="intensity-value">
          {textIntensity} / 10
        </span>
      </div>

      <div className="question-block">
        <label>
          How long have you felt this way?
        </label>

        <select
          value={textDuration}
          onChange={(e) =>
            setTextDuration(e.target.value)
          }
        >
          <option value="">
            Select Duration
          </option>

          <option value="Few Minutes">
            Few Minutes
          </option>

          <option value="Several Hours">
            Several Hours
          </option>

          <option value="Today">
            Today
          </option>

          <option value="Several Days">
            Several Days
          </option>

          <option value="Weeks+">
            Weeks+
          </option>
        </select>
      </div>

      <div className="insight-card">
        💡 Tell EmoTrack AI more about your situation.
        The journal entry is the most important part
        of the text analysis.
      </div>

      <textarea
  value={journal}
  onChange={(e) => {
    if (!typingStartTime) {
      setTypingStartTime(Date.now());
    }

    setJournal(e.target.value);

    const elapsed =
      (Date.now() - typingStartTime) / 60000;

    const words =
      e.target.value.trim().split(/\s+/).length;

    if (elapsed > 0) {
      setTypingSpeed(
        Math.round(words / elapsed)
      );
    }
  }}
  maxLength={800}
  placeholder="Describe what happened, how you are feeling, and what is on your mind today..."
/>

      <div className="char-count">
        {journal.length}/800 characters
      </div>
      <div className="char-count">
      Typing Speed: {typingSpeed} WPM
       </div>

      <button
        className="primary-action full"
        onClick={onNext}
      >
        Continue
      </button>

    </div>
  </div>

  );
  }


function ProcessingStep({ loading, analyzeEmotion }) {
  const items = [
    "Pulse Analysis Complete",
    "Face Analysis Complete",
    "Voice Analysis Complete",
    "Text Analysis Complete",
    "Fusion Complete",
    "Recommendation Engine Complete",
  ];

  return (
    <div className="processing-screen">
      <motion.div className="processing-core" animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 8, ease: "linear" }}>
        <Brain size={42} />
      </motion.div>
      <h2>AI Processing</h2>
      <p>Combining multimodal signals into one clinical-grade wellness readout.</p>
      <div className="processing-list">
        {items.map((item) => (
          <div key={item}>
            <CheckCircle2 size={18} />
            <span>{item}</span>
          </div>
        ))}
      </div>
      <button className="primary-action" onClick={analyzeEmotion} disabled={loading}>
        {loading ? "Analyzing..." : "Run Fusion Analysis"}
      </button>
    </div>
  );
}

function ResultsAndRecommendations({
  finalResult,
  confidence,
  stressScore,
  faceResult,
  voiceResult,
  dashboardData,
  emotionDistribution,
  modalityScores,
  wellnessMetrics,
}) {
  return (
    <div className="stack">
      <ResultReport
        finalResult={finalResult}
        confidence={confidence}
        stressScore={stressScore}
        faceResult={faceResult}
        voiceResult={voiceResult}
        dashboardData={dashboardData}
        emotionDistribution={emotionDistribution}
        modalityScores={modalityScores}
        wellnessMetrics={wellnessMetrics}
      />
      <RecommendationGrid />
    </div>
  );
}

function ResultReport({

 finalResult,

 confidence,

 stressScore,

 faceResult,

 voiceResult,

 dashboardData,

 emotionDistribution,

 modalityScores,

 wellnessMetrics
}) {
  const emotion = finalResult.final_emotion || dashboardData?.latest_emotion || "N/A";
  const scores = modalityScores?.length
    ? modalityScores
    : modalityScoresFromResult(faceResult, voiceResult, finalResult, dashboardData);
  const metrics = wellnessMetrics?.length
    ? wellnessMetrics
    : [
        { label: "Stress Score", value: stressScore },
        { label: "Wellness Score", value: Math.max(0, 100 - stressScore) },
      ];

  return (
    <div className="stack">
      <section className="report-hero">
        <div>
          <p className="eyebrow">Final emotion</p>
          <h2>{emotion}</h2>
          <p>Confidence score: {confidence}%</p>
        </div>
        <div className="confidence-ring" style={{ "--score": `${confidence}%` }}>
          <strong>{confidence}%</strong>
          <span>Confidence</span>
        </div>
      </section>

      <section className="analytics-grid two">
        <ChartPanel title="Fusion Analysis">
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie data={emotionDistribution || []} dataKey="value" innerRadius={62} outerRadius={94}>
                {emotionDistribution.map((entry) => (
                  <Cell key={entry.name} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </ChartPanel>
        <ChartPanel title="Modality Radar">
          <ResponsiveContainer width="100%" height={260}>
            <RadarChart data={scores}>
              <PolarGrid />
              <PolarAngleAxis dataKey="metric" />
              <PolarRadiusAxis angle={30} domain={[0, 100]} />
              <Radar dataKey="score" stroke="#6366f1" fill="#6366f1" fillOpacity={0.35} />
            </RadarChart>
          </ResponsiveContainer>
        </ChartPanel>
      </section>

      <section className="kpi-grid">

  {scores.map(({ metric, score }) => (

    <div
      className="contribution-card"
      key={metric}
    >

      <span>{metric}</span>

      <strong>{score}%</strong>

      <div>

        <i
          style={{
            width: `${score}%`
          }}
        />

      </div>

    </div>

  ))}

</section>

      <section className="wellness-grid">
        {metrics.map(({ label, value }) => (
          <div className="wellness-metric" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
          </div>
        ))}
      </section>
    </div>
  );
}

function RecommendationGrid() {
  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Recommendations</p>
          <h3>Personalized next best actions</h3>
        </div>
      </div>
      <div className="recommendation-grid">
        {recommendations.map((item) => {
          const Icon = item.icon;
          return (
            <article className="recommendation-card" key={item.title}>
              <Icon size={22} />
              <h4>{item.title}</h4>
              <p>{item.description}</p>
              <button>{item.cta}</button>
            </article>
          );
        })}
      </div>
    </section>
  );
}

function Insights({ trendData, emotionDistribution }) {
  return (
    <div className="stack">
      <section className="analytics-grid two">
        <ChartPanel title="Weekly Trends">
          <ResponsiveContainer width="100%" height={260}>
            <AreaChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="day" />
              <YAxis hide />
              <Tooltip />
              <Area dataKey="mood" stroke="#14b8a6" fill="#14b8a655" strokeWidth={3} />
            </AreaChart>
          </ResponsiveContainer>
        </ChartPanel>
        <ChartPanel title="Monthly Stress Trends">
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="day" />
              <YAxis hide />
              <Tooltip />
              <Bar dataKey="stress" fill="#f97316" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartPanel>
      </section>
      <section className="insights-grid">
        <div className="panel">
          <p className="eyebrow">Calendar heatmap</p>
          <div className="heatmap">
            {Array.from({ length: 35 }, (_, index) => (
              <span key={index} className={`heat-${index % 5}`} />
            ))}
          </div>
        </div>
        <div className="panel">
          <p className="eyebrow">AI insights</p>
          <h3>Patterns worth watching</h3>
          <p className="muted">
            {trendData?.length
              ? `Latest saved assessment is ${trendData[trendData.length - 1].emotion} with a ${trendData[trendData.length - 1].stress}/100 stress score.`
              : "Run assessments to generate database-backed insights."}
          </p>
        </div>
      </section>
      <section className="analytics-grid two">
        <ChartPanel title="Mood History">
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={trendData}>
              <XAxis dataKey="day" />
              <YAxis hide />
              <Tooltip />
              <Line dataKey="mood" stroke="#22c55e" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </ChartPanel>
        <ChartPanel title="Emotion Distribution">
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie data={emotionDistribution} dataKey="value" innerRadius={54} outerRadius={82}>
                {emotionDistribution.map((entry) => (
                  <Cell key={entry.name} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </ChartPanel>
      </section>
    </div>
  );
}

function Reports({ reports, searchTerm, setSearchTerm, sortKey, setSortKey, filterStatus, setFilterStatus }) {
  return (
    <div className="panel">
      <div className="table-toolbar">
        <div className="search-box">
          <Search size={17} />
          <input value={searchTerm} onChange={(event) => setSearchTerm(event.target.value)} placeholder="Search reports" />
        </div>
        <select value={sortKey} onChange={(event) => setSortKey(event.target.value)}>
          <option value="date">Sort by date</option>
          <option value="wellness">Sort by wellness</option>
          <option value="stress">Sort by stress</option>
        </select>
        <select value={filterStatus} onChange={(event) => setFilterStatus(event.target.value)}>
          <option>All</option>
          <option>Complete</option>
          <option>Reviewed</option>
          <option>Flagged</option>
        </select>
        <button className="secondary-action">
          <Download size={17} />
          Export PDF
        </button>
      </div>
      <div className="report-table">
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Emotion</th>
              <th>Wellness Score</th>
              <th>Stress Score</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {reports.map((report) => (
              <tr key={report.id || `${report.rawDate}-${report.emotion}`}>
                <td>{report.date}</td>
                <td>{report.emotion}</td>
                <td>{report.wellness}</td>
                <td>{report.stress}</td>
                <td>
                  <span className={`status ${report.status.toLowerCase()}`}>{report.status}</span>
                </td>
                <td>
                  <button className="link-button">View Report</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function Goals() {
  return (
    <div className="goals-grid">
      {[
        ["Daily Mood Check-In", "5 of 7 days complete", CalendarDays],
        ["Wellness Streaks", "12 day active streak", Flame],
        ["Achievement Badges", "Calm week unlocked", Sparkles],
        ["Goal Tracking", "Sleep consistency at 78%", Target],
      ].map(([title, detail, Icon]) => (
        <div className="panel goal-card" key={title}>
          <Icon size={22} />
          <h3>{title}</h3>
          <p>{detail}</p>
          <div className="goal-progress">
            <i />
          </div>
        </div>
      ))}
      <div className="emergency-card">
        <ShieldAlert size={24} />
        <div>
          <h3>Emergency Support</h3>
          <p>For urgent distress, contact local emergency services or a trusted support line immediately.</p>
        </div>
      </div>
    </div>
  );
}

function Profile() {
  return (
    <div className="profile-grid">
      <div className="panel profile-card">
        <div className="avatar">V</div>
        <h2>Alex</h2>
        <p>Patient wellness profile</p>
      </div>
      {[
        ["User Information", "Age, care preferences, baseline mood"],
        ["Wellness Statistics", "24 assessments, 86 average score"],
        ["Connected Devices", "Wearable pulse monitor connected"],
        ["Notification Preferences", "Daily check-in and weekly report"],
        ["Privacy Settings", "Encrypted health data controls"],
      ].map(([title, detail]) => (
        <div className="panel" key={title}>
          <h3>{title}</h3>
          <p className="muted">{detail}</p>
        </div>
      ))}
    </div>
  );
}

function SettingsView() {
  return (
    <div className="settings-grid">
      {[
        ["Clinical Data Privacy", "Manage consent, storage, and sharing.", Lock],
        ["Notifications", "Tune alerts and wellness reminders.", Bell],
        ["Assistant Preferences", "Personalize tone and support depth.", Brain],
      ].map(([title, detail, Icon]) => (
        <div className="panel settings-card" key={title}>
          <Icon size={22} />
          <h3>{title}</h3>
          <p className="muted">{detail}</p>
          <label className="switch">
            <input type="checkbox" defaultChecked />
            <span />
          </label>
        </div>
      ))}
    </div>
  );
}

function Help() {
  return (
    <div className="help-grid">
      <div className="panel">
        <p className="eyebrow">Help & Support</p>
        <h2>Care team support center</h2>
        <p className="muted">Find guidance for assessments, reports, privacy, and device connections.</p>
      </div>
      <div className="emergency-card">
        <ShieldAlert size={24} />
        <div>
          <h3>Emergency Support</h3>
          <p>If you may harm yourself or someone else, seek immediate emergency help now.</p>
        </div>
      </div>
    </div>
  );
}

function ChartPanel({ title, children }) {
  return (
    <div className="panel chart-panel">
      <div className="panel-header">
        <h3>{title}</h3>
      </div>
      {children}
    </div>
  );
}

function AssistantWidget() {
  return (
    <motion.div className="assistant-widget" initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }}>
      <Waves size={18} />
      <div>
        <strong>AI Wellness Assistant</strong>
        <span>Ready for a check-in</span>
      </div>
    </motion.div>
  );
}

export default App;
