<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Voice Cloning Detection Prototype</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header>
    <h1>AI-Powered Real-Time Voice Cloning Detection</h1>
    <p>Prototype &middot; R.M.K. Engineering College &middot; Information Technology</p>
  </header>

  <main>
    <div id="modeBanner" class="banner">Checking server...</div>

    <section class="card">
      <h2>1. Live microphone check</h2>
      <p>Speak (or play a call on speaker). The audio is analysed every 3 seconds.</p>
      <button id="startBtn">Start listening</button>
      <button id="stopBtn" disabled>Stop</button>
      <span id="liveStatus"></span>
    </section>

    <section class="card">
      <h2>2. Upload an audio file</h2>
      <input type="file" id="fileInput" accept="audio/*">
      <button id="uploadBtn">Analyse file</button>
    </section>

    <section class="card" id="resultCard">
      <h2>Result</h2>
      <div id="riskBox" class="risk none">NO DATA</div>
      <div class="bar"><div id="barFill"></div></div>
      <p>Cloned-voice probability: <b id="scoreText">--</b></p>
      <p id="advice">Start the microphone or upload a file to see a result.</p>

      <h3>Segment timeline</h3>
      <table>
        <thead><tr><th>Time (s)</th><th>Fake probability</th><th>Level</th></tr></thead>
        <tbody id="segBody"></tbody>
      </table>
    </section>

    <p class="note">This is an extra security layer, not proof. Always verify sensitive requests
      (money, OTPs, passwords) by calling the person back on a known number.</p>
  </main>

  <script src="app.js"></script>
</body>
</html>