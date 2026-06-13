const API = 'http://localhost:8000/api'

// ── DOM refs ──────────────────────────────────────────────
const inputResume = document.getElementById('input-resume')
const inputVideo  = document.getElementById('input-video')
const nameResume  = document.getElementById('name-resume')
const nameVideo   = document.getElementById('name-video')
const boxResume   = document.getElementById('box-resume')
const boxVideo    = document.getElementById('box-video')
const btnAnalyze  = document.getElementById('btn-analyze')
const btnReset    = document.getElementById('btn-reset')
const errorBox    = document.getElementById('error-box')

const secUpload   = document.getElementById('section-upload')
const secProgress = document.getElementById('section-progress')
const secResults  = document.getElementById('section-results')

const stepResume  = document.getElementById('step-resume')
const stepVideo   = document.getElementById('step-video')
const stepScoring = document.getElementById('step-scoring')

// ── File selection ────────────────────────────────────────
inputResume.addEventListener('change', () => {
  const file = inputResume.files[0]
  if (file) {
    nameResume.textContent = file.name
    boxResume.classList.add('has-file')
  }
  updateAnalyzeBtn()
})

inputVideo.addEventListener('change', () => {
  const file = inputVideo.files[0]
  if (file) {
    nameVideo.textContent = file.name
    boxVideo.classList.add('has-file')
  }
  updateAnalyzeBtn()
})

function updateAnalyzeBtn() {
  btnAnalyze.disabled = !(inputResume.files.length > 0 && inputVideo.files.length > 0)
}

// ── Main analyze flow ─────────────────────────────────────
btnAnalyze.addEventListener('click', async () => {
  hideError()
  showSection('progress')
  resetSteps()

  try {
    // Step 1 — Upload & parse resume
    setStep(stepResume, 'active')
    const resumeData = await uploadResume(inputResume.files[0])
    setStep(stepResume, 'done')

    // Step 2 — Upload & transcribe video
    setStep(stepVideo, 'active')
    const videoData = await uploadVideo(inputVideo.files[0])
    setStep(stepVideo, 'done')

    // Step 3 — Score with Gemini
    setStep(stepScoring, 'active')
    const result = await analyzeCandidate(resumeData.resume_text, videoData.transcript)
    setStep(stepScoring, 'done')

    // Render and show results
    renderResults(result)
    showSection('results')

  } catch (err) {
    showSection('upload')
    showError(err.message || 'Something went wrong. Please try again.')
  }
})

// ── Reset ─────────────────────────────────────────────────
btnReset.addEventListener('click', () => {
  inputResume.value = ''
  inputVideo.value  = ''
  nameResume.textContent = 'No file chosen'
  nameVideo.textContent  = 'No file chosen'
  boxResume.classList.remove('has-file')
  boxVideo.classList.remove('has-file')
  btnAnalyze.disabled = true
  hideError()
  showSection('upload')
})

// ── API calls ─────────────────────────────────────────────
async function uploadResume(file) {
  const form = new FormData()
  form.append('file', file)

  const res = await fetch(`${API}/upload/resume`, { method: 'POST', body: form })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `Resume upload failed (${res.status})`)
  }
  return res.json()
}

async function uploadVideo(file) {
  const form = new FormData()
  form.append('file', file)

  const res = await fetch(`${API}/upload/video`, { method: 'POST', body: form })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `Video upload failed (${res.status})`)
  }
  return res.json()
}

async function analyzeCandidate(resumeText, transcript) {
  const res = await fetch(`${API}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ resume_text: resumeText, transcript }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `Analysis failed (${res.status})`)
  }
  return res.json()
}

// ── Render results ────────────────────────────────────────
function renderResults(data) {
  // Name + recommendation badge
  document.getElementById('result-name').textContent =
    data.candidate_name || 'Candidate'

  const badge = document.getElementById('result-recommendation')
  badge.textContent = data.recommendation
  badge.className = 'badge'
  if      (data.recommendation === 'Strong Hire') badge.classList.add('hire')
  else if (data.recommendation === 'Consider')    badge.classList.add('consider')
  else                                             badge.classList.add('pass')

  // Overall score
  document.getElementById('result-overall').textContent = data.scores.overall

  // Summary
  document.getElementById('result-summary').textContent = data.summary

  // Strengths list
  const ulS = document.getElementById('result-strengths')
  ulS.innerHTML = ''
  ;(data.strengths || []).forEach(s => {
    const li = document.createElement('li')
    li.textContent = s
    ulS.appendChild(li)
  })

  // Weaknesses list
  const ulW = document.getElementById('result-weaknesses')
  ulW.innerHTML = ''
  ;(data.weaknesses || []).forEach(w => {
    const li = document.createElement('li')
    li.textContent = w
    ulW.appendChild(li)
  })

  // Score bars — short delay so CSS transition plays
  setTimeout(() => {
    setBar('technical',    data.scores.technical_skills)
    setBar('communication', data.scores.communication)
    setBar('experience',   data.scores.experience_relevance)
    setBar('projects',     data.scores.project_quality)
  }, 120)

  // Consistency note
  document.getElementById('result-consistency').textContent =
    data.consistency_note
}

function setBar(key, value) {
  document.getElementById(`bar-${key}`).style.width = `${value * 10}%`
  document.getElementById(`num-${key}`).textContent  = `${value}/10`
}

// ── UI helpers ────────────────────────────────────────────
function showSection(name) {
  secUpload.classList.add('hidden')
  secProgress.classList.add('hidden')
  secResults.classList.add('hidden')
  if (name === 'upload')   secUpload.classList.remove('hidden')
  if (name === 'progress') secProgress.classList.remove('hidden')
  if (name === 'results')  secResults.classList.remove('hidden')
}

function setStep(el, state) {
  el.classList.remove('active', 'done')
  if (state) el.classList.add(state)
}

function resetSteps() {
  ;[stepResume, stepVideo, stepScoring].forEach(s =>
    s.classList.remove('active', 'done')
  )
}

function showError(msg) {
  errorBox.textContent = `⚠️ ${msg}`
  errorBox.classList.remove('hidden')
}

function hideError() {
  errorBox.classList.add('hidden')
  errorBox.textContent = ''
}
