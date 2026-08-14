/* Career Recommendation System - browser-side controller */
(() => {
    "use strict";

    const state = { careers: [], userSkills: [] };
    const charts = {};
    const elements = {
        skillInput: document.querySelector("#skillinputbar"),
        addSkills: document.querySelector("#skillinputbtn"),
        fileInput: document.querySelector("#file-upload"),
        fileLabel: document.querySelector("#file-upload-label"),
        career: document.querySelector("#careerinputbar"),
        analyze: document.querySelector("#Analyze"),
        year: document.querySelector("#year"),
        skillGap: document.querySelector("#skill-gap-content"),
        gaugeValue: document.querySelector("#gauge-value"),
        readinessMessage: document.querySelector("#readiness-message"),
        matchEmpty: document.querySelector("#match-empty"),
        bestMatch: document.querySelector("#best-match"),
        courseContent: document.querySelector("#course-content"),
        roadmapContent: document.querySelector("#roadmap-content")
    };

    const normalise = value => value.trim().replace(/\s+/g, " ").toLowerCase();
    const escapeHtml = value => String(value).replace(/[&<>'"]/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#039;", '"': "&quot;" })[char]);
    const unique = values => [...new Map(values.map(value => [normalise(value), value.trim()])).values()];

    function destroyChart(name) {
        if (charts[name]) charts[name].destroy();
    }

    function renderReadinessGauge(score) {
        const canvas = document.querySelector("#readiness-chart");
        if (!canvas || !window.Chart) return;
        destroyChart("readiness");
        const colour = score >= 80 ? "#5b8c5a" : score >= 50 ? "#c99b45" : "#b85b5b";
        charts.readiness = new Chart(canvas, {
            type: "doughnut",
            data: { datasets: [{ data: [score, 100 - score], backgroundColor: [colour, "#e8dfd0"], borderWidth: 0, borderRadius: 8 }] },
            options: {
                responsive: true, maintainAspectRatio: false, cutout: "75%", rotation: -90, circumference: 180,
                plugins: { legend: { display: false }, tooltip: { enabled: false } }
            }
        });
    }

    function renderMatchChart(matches) {
        const canvas = document.querySelector("#match-chart");
        if (!canvas || !window.Chart) return;
        destroyChart("matches");
        charts.matches = new Chart(canvas, {
            type: "bar",
            data: { labels: matches.map(item => item.career), datasets: [{ data: matches.map(item => item.score), backgroundColor: "#dcc6a0", borderRadius: 8, borderSkipped: false }] },
            options: {
                indexAxis: "y", responsive: true, maintainAspectRatio: false,
                scales: { x: { beginAtZero: true, max: 100, grid: { color: "#e8dfd0" }, ticks: { callback: value => `${value}%` } }, y: { grid: { display: false } } },
                plugins: { legend: { display: false }, tooltip: { callbacks: { label: context => `${context.raw.toFixed(1)}% match` } } }
            }
        });
    }

    function months(value) {
        const number = Number.parseInt(value, 10) || 0;
        return value.toLowerCase().includes("year") ? number * 12 : number;
    }

    function renderInsightsChart(insights) {
        const canvas = document.querySelector("#insights-chart");
        if (!canvas || !window.Chart) return;
        destroyChart("insights");
        const difficultyColours = { Low: "#5b8c5a", Medium: "#c99b45", High: "#c7773b", "Very High": "#b85b5b" };
        charts.insights = new Chart(canvas, {
            type: "bar",
            data: {
                labels: insights.map(item => item.career),
                datasets: [{ label: "Learning time (months)", data: insights.map(item => months(item.learning_time || "0")), backgroundColor: insights.map(item => difficultyColours[item.difficulty] || "#dcc6a0"), borderRadius: 8 }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                scales: { y: { beginAtZero: true, grid: { color: "#e8dfd0" } }, x: { grid: { display: false }, ticks: { maxRotation: 35, minRotation: 35 } } },
                plugins: { legend: { display: false }, tooltip: { callbacks: { label: context => `${context.raw} month(s)` } } }
            }
        });
    }

    function showMessage(message, type = "info") {
        const notice = document.querySelector("#app-notice") || document.createElement("p");
        notice.id = "app-notice";
        notice.setAttribute("role", "status");
        notice.textContent = message;
        notice.style.cssText = `text-align:center;margin:1rem auto;color:${type === "error" ? "#a12c2c" : "#2e2a24"};font-weight:500;`;
        elements.analyze.parentElement.after(notice);
    }

    async function requestApi(url, options = {}) {
        const response = await fetch(url, options);
        const payload = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error(payload.error || "Something went wrong. Please try again.");
        return payload;
    }

    async function initialise() {
        elements.year.textContent = new Date().getFullYear();
        try {
            const data = await requestApi("/api/careers");
            state.careers = data.careers;
            const careerNames = state.careers.sort((a, b) => a.localeCompare(b));
            elements.career.innerHTML = '<option value="">Select a target career</option>' + careerNames
                .map(name => `<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`).join("");
            elements.career.disabled = false;
        } catch (error) {
            console.error(error);
            showMessage("The application server could not be reached. Start it with: python app.py", "error");
        }
    }

    function updateSkills(input) {
        const entered = input.split(/[,\n;]+/).map(value => value.trim()).filter(Boolean);
        state.userSkills = unique(entered);
        if (state.userSkills.length) {
            document.querySelector("#app-notice")?.remove();
        } else {
            showMessage("Add at least one skill to continue.", "error");
        }
    }

    async function handleResume(event) {
        const [file] = event.target.files;
        if (!file) return;
        if (file.type !== "application/pdf" && !file.name.toLowerCase().endsWith(".pdf")) {
            event.target.value = "";
            showMessage("Please upload a PDF resume.", "error");
            return;
        }
        elements.fileLabel.textContent = "Reading resume...";
        try {
            const formData = new FormData();
            formData.append("resume", file);
            const data = await requestApi("/api/resume-skills", { method: "POST", body: formData });
            state.userSkills = unique(data.skills || []);
            if (!state.userSkills.length) throw new Error("No recognised skills found");
            elements.skillInput.value = state.userSkills.join(", ");
            showMessage(`Found ${state.userSkills.length} skill(s) in ${file.name}.`);
        } catch (error) {
            console.error(error);
            showMessage("Could not read skills from this PDF. Please enter your skills manually.", "error");
        } finally {
            elements.fileLabel.textContent = "Upload File";
        }
    }

    function renderResults(data) {
        const missing = data.missing_skills;
        const topFive = data.top_matches;
        const courses = data.recommended_courses;

        elements.skillGap.innerHTML = missing.length
            ? `<p>${missing.map(escapeHtml).join(" • ")}</p><small>${missing.length} skill(s) to develop</small>`
            : "<p>You have every listed skill for this career. Great work!</p>";
        elements.gaugeValue.innerHTML = `${data.readiness_score.toFixed(1)}<small>%</small>`;
        elements.readinessMessage.textContent = data.readiness_score >= 80 ? "Excellent readiness!" : data.readiness_score >= 50 ? "You are on the right track." : "Focus on the missing skills below.";
        elements.matchEmpty.hidden = topFive.length > 0;
        elements.bestMatch.innerHTML = topFive.length
            ? `<strong>Best match:</strong> ${escapeHtml(topFive[0].career)} <span>${topFive[0].score.toFixed(1)}% match</span>`
            : "Career insights will appear after a match is found.";
        elements.courseContent.innerHTML = courses.length
            ? `<ul>${courses.slice(0, 8).map(course => `<li><a href="${escapeHtml(course.link)}" target="_blank" rel="noopener">${escapeHtml(course.course)}</a> — ${escapeHtml(course.skill)} (${escapeHtml(course.provider)})</li>`).join("")}</ul>`
            : "<p>No course matches were found for the current skill gap.</p>";
        elements.roadmapContent.innerHTML = data.roadmap.length
            ? `<div class="roadmap-path" role="list">${data.roadmap.map(item => `<article class="roadmap-node" role="listitem"><span class="roadmap-month">${item.month}</span><div class="roadmap-detail"><small>MONTH ${item.month}</small><strong>${escapeHtml(item.skill)}</strong></div></article>`).join("")}</div>`
            : "<p>Your roadmap is complete for this selected career.</p>";
        renderReadinessGauge(data.readiness_score);
        renderMatchChart(topFive);
        renderInsightsChart(data.career_insights);
        const resultsSection = document.querySelector("#features");
        resultsSection.hidden = false;
        resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    elements.addSkills.addEventListener("click", () => updateSkills(elements.skillInput.value));
    elements.skillInput.addEventListener("keydown", event => { if (event.key === "Enter") { event.preventDefault(); updateSkills(elements.skillInput.value); } });
    elements.fileInput.addEventListener("change", handleResume);
    elements.analyze.addEventListener("click", async () => {
        if (!state.careers.length) return showMessage("Career data is still loading.", "error");
        updateSkills(elements.skillInput.value || state.userSkills.join(","));
        if (!state.userSkills.length) return;
        if (!elements.career.value) return showMessage("Please select your target career.", "error");
        elements.analyze.disabled = true;
        elements.analyze.textContent = "Analyzing...";
        try {
            const result = await requestApi("/api/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ skills: state.userSkills, target_career: elements.career.value })
            });
            renderResults(result);
        } catch (error) {
            showMessage(error.message, "error");
        } finally {
            elements.analyze.disabled = false;
            elements.analyze.textContent = "Analyze";
        }
    });
    initialise();
})();
