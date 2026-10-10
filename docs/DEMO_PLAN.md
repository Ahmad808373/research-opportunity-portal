# Real demonstration recording: target 58 seconds

The actual recording is pending. This is a plan, not a claim that a video exists.
The PDF permits approximately one minute and explicitly says not to exceed one minute.

## Prepare before recording

1. Follow README setup and run the real MySQL/Flask application on Windows.
2. Import the Postman collection, set base_url, and run it once to confirm it passes.
   Two stored records will remain; verify them in the frontend. The eight mandatory
   scenarios are requests 01-10, including three POST requests.
3. Arrange Flask's running terminal beside your browser so its address is readable.
   Open a second ready-to-switch window/tab for Postman Collection Runner.
4. Open Add Opportunity and fill all fields, leaving Save for the actual recording:
   title Campus Network Study; description Study congestion in the campus network;
   area Networks; faculty Example Faculty; department Computer Science; skills
   Python and Wireshark; positions 2; deadline 2026-12-20; status Open.
5. Prepare a small title edit (Campus Network Study - Updated). Avoid slow typing:
   copy that text to the clipboard before recording or use a short edit such as
   adding "Updated". Know where Close and Delete appear in details.
6. In Postman, select the full collection for one iteration. Keep requests 09 and
   10 easy to open after the run to display their actual response bodies.
7. Rehearse once. Confirm the three-layer app works locally before recording.

## Timeline

| Time | Screen and action | Optional narration |
|---|---|---|
| 00-04 | Show running Flask terminal with the local server address and the application beside it | "Flask runs locally and connects to MySQL." |
| 04-10 | Show the prefilled Add Opportunity form; click Save; show success and the new card | "This form creates a database record through POST." |
| 10-15 | Show the list and click View details on the new opportunity | "GET retrieves the stored list and full details." |
| 15-23 | Click Edit; change the title; Save; show updated title | "PUT updates the stored opportunity." |
| 23-28 | Click Close Opportunity; show Closed in the list and details | "A status-only PUT closes the opening." |
| 28-34 | Click Delete; confirm; show success and its removal | "DELETE removes the record from MySQL." |
| 34-40 | Switch to ready Postman Runner; click Run for requests 01-14 | "The collection tests all required API scenarios, starting with three creates." |
| 40-47 | Show the completed run's passing requests/tests; select successful POST and its 201 JSON if time permits | "Responses include generated IDs and appropriate status codes." |
| 47-53 | Open request 09's response from the run; show 404 and Opportunity not found | "Retrieving the deleted ID returns 404." |
| 53-58 | Open request 10's response from the run; show 400 and missing-field message; stop recording | "Invalid input is rejected with an explanation." |

Do not replace the actual responses with screenshots or manually edited text.
Runner responses must be from your live recording's run. If switching views takes
too long, focus on Runner summary plus request 09's 404; one 400 or 404 error is
enough for the video, while the collection retains both tested scenarios.

## Recording on Windows

Use any screen recorder already available that captures the full desktop so
switching between Flask, the browser, and Postman stays visible. A full-desktop
recorder is more suitable than a tool restricted to a single app window. Open the
recorder, select the desktop region, and start recording. Follow the sequence and
stop at about 58 seconds. Narration is optional; visible operations are essential.

Play the saved MP4 and check its **actual duration** in the player's file/properties
display. It must be <=60 seconds, with every required action still visible. Trim
only idle time at the beginning/end if necessary, then check the exported file's
duration again. Inspect readability, real response codes, and accidental exposure
of private windows or .env before submission.

Save it as demo.mp4 or provide a video link your instructor can open without
requesting access. Include the actual video or accessible link in the final ZIP.
