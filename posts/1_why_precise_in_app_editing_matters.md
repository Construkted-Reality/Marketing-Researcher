**Cut and Shape 3D Models in Metashape for Accurate Photogrammetry Results**  

*Target audience: Photogrammetry practitioners who need clean, editable meshes without spending hours in a full‑blown 3D‑modeling suite.*

---

Photogrammetry has come a long way from the days when a handful of overlapping photos produced a rough point cloud that required a specialist’s touch to become usable. Today, the bottleneck is no longer “getting the data” but “getting the data right.” Users repeatedly complain about stray geometry, unwanted background points, and the inability to carve precise holes for doors, windows, or interior voids without resorting to external CAD tools. Those pain points linger even after a dense cloud is generated, because most photogrammetry pipelines stop at “export mesh.”  

Agisoft Metashape (formerly PhotoScan) offers a set of **shape‑drawing** and **cutting** tools that let you edit a mesh directly inside the software—no need to jump to Blender or Maya for a quick clean‑up. This tutorial walks you through those tools step by step, explains why they matter for the most common user frustrations, and shows where **Construkted Reality** fits into the broader workflow as a collaborative, web‑based hub for the final assets.

---

## 1. Why Precise In‑App Editing Matters  

| Typical complaint | Root cause | How Metashape’s shape tools help |
|-------------------|------------|----------------------------------|
| “My mesh has a lot of background noise that shows up as floating islands.” | Tie points are generated on non‑target surfaces (e.g., sky, distant trees). | Polygon‑drawn masks let you isolate and delete those islands without re‑running the whole workflow. |
| “I need a clean hole for a doorway, but the mesh is a solid slab.” | Dense cloud fills every visible surface; no concept of “voids.” | The **Cut** operation removes selected faces and automatically stitches the surrounding geometry. |
| “Every time I edit the model I lose the original metadata.” | Exporting to a separate editor strips georeferencing and capture info. | Metashape keeps the asset’s geo‑tags intact while you edit, preserving the link to the original photos. |

A recent forum thread on creating clean holes illustrates the frustration: a user posted a mesh with a “messy” opening and was told that Metashape’s built‑in cutter could solve the problem, but the explanation was “unusable” ([Agisoft Forum, 2024](https://www.agisoft.com/forum/index.php?topic=16735.0)). This tutorial fills that gap with a concrete, reproducible workflow.

---

## 2. Quick Overview of Metashape’s Shape‑Drawing & Cutting Toolbox  

Metashape’s **Model** tab houses three primary shape tools:

1. **Polygon** – click to place vertices; close the loop to define an arbitrary area.  
2. **Rectangle** – click‑drag to create an axis‑aligned box.  
3. **Circle** – click‑drag to set centre and radius.

Once a shape is drawn, the **Edit** menu offers:

* **Delete** – removes faces inside the shape.  
* **Cut** – slices the mesh along the shape’s boundary, creating a clean edge.  
* **Extract** – isolates the selected region as a separate mesh (useful for sub‑assemblies).  

These operations work on the **mesh** layer, not the dense cloud, which means they are fast and preserve the underlying point data for later re‑generation if needed.

---

## 3. Step‑by‑Step Tutorial  

Below is a complete, production‑ready pipeline. Screenshots are represented by placeholders; you can replace them with actual captures when publishing.

### 3.1. Prepare Your Photo Set  

1. **Import images** (`File → Add Photos`). Ensure EXIF data is intact; Metashape reads GPS tags automatically.  
2. **Align photos** (`Workflow → Align Photos`). Use *High* accuracy for most projects; *Medium* is sufficient for quick tests.  
3. **Build dense cloud** (`Workflow → Build Dense Cloud`). Choose *High* quality if you have a decent GPU; otherwise *Medium* balances speed and detail.  

> *Tip:* If you notice stray tie points on the horizon, mask those regions before alignment (Ctrl L) as described in the Geo‑SfM tutorial ([UniSvalbard, n.d.](https://unisvalbard.github.io/Geo-SfM/content/lessons/tutorial/tutorial.html)).

[IMAGE 1] – *Alignment view with tie points highlighted.*

### 3.2. Generate the Mesh  

1. **Build mesh** (`Workflow → Build Mesh`). Select *Arbitrary* surface type for most objects; switch to *Height Field* for terrain.  
2. Set **Face count** to *High* for detailed models; the “Ultra” setting is rarely needed and can cause memory spikes ([Agisoft Forum, 2017](https://www.agisoft.com/forum/index.php?topic=6409.0)).  
3. Enable **UV mapping** if you plan to texture later.  

[IMAGE 2] – *Mesh preview with texture applied.*

### 3.3. Activate the Shape‑Drawing Toolbar  

1. Switch to the **Model** tab.  
2. Click the **Shape** icon (looks like a polygon). Choose **Polygon**, **Rectangle**, or **Circle** depending on the geometry you need to isolate.  

[IMAGE 3] – *Shape‑drawing toolbar highlighted.*

### 3.4. Drawing a Precise Selection  

**Example:** Cutting a doorway in a building façade.  

1. Zoom to the façade.  
2. Select **Rectangle** and drag a box that exactly covers the door opening.  
3. Press **Enter** to confirm the shape.  

If the door is irregular, switch to **Polygon** and click around the frame, snapping to existing vertices for accuracy. Metashape shows a live preview of the selected faces in magenta.  

[IMAGE 4] – *Rectangle drawn around a door opening.*

### 3.5. Executing the Cut  

1. With the shape still active, go to **Edit → Cut**.  
2. Metashape will slice the mesh along the rectangle’s edges, leaving a clean void.  
3. Inspect the result; you should see a crisp, planar opening.  

If you need to *remove* the interior geometry entirely (e.g., a window that should be empty), use **Delete** instead of **Cut**.  

[IMAGE 5] – *Resulting clean doorway after Cut.*

### 3.6. Refining the Edge  

Even after a perfect cut, the surrounding vertices may be uneven.  

* **Smooth** – `Tools → Mesh → Smooth` (apply a low iteration count to avoid flattening details).  
* **Decimate** – `Tools → Mesh → Reduce Face Count` if the cut introduced unnecessary high‑density triangles.  

These operations keep the mesh lightweight for web visualization, a key consideration for platforms like **Construkted Reality** where storage fees are tier‑based.

### 3.7. Exporting the Edited Mesh  

1. **File → Export Model**. Choose **OBJ**, **FBX**, or **PLY** based on downstream needs.  
2. Tick **Export UV** and **Export Camera Positions** to retain texture mapping and georeferencing.  

Your cleaned, geotagged mesh is now ready for upload to Construkted Reality’s asset library.

[IMAGE 6] – *Export dialog with metadata options checked.*

---

## 4. Common Pitfalls & How to Solve Them  

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Cut leaves a jagged edge | Shape not aligned to mesh topology | Snap shape vertices to existing mesh edges (hold **Ctrl** while drawing). |
| Deleted faces reappear after re‑building mesh | Dense cloud still contains points in the cut region | Use **Mask** on the dense cloud before building the mesh, or rebuild the mesh after editing. |
| Exported model loses GPS coordinates | Export format does not support georeferencing (e.g., generic OBJ) | Export as **FBX** with “Export Camera Positions” enabled, or keep a separate **.txt** with coordinate metadata. |

A Reddit user reported “lumpy” surfaces after dense cloud generation, suspecting that too many tie points caused the issue ([Reddit, 2024](https://www.reddit.com/r/photogrammetry/comments/ws36ga/metashape_best_settings/)). The consensus is to **optimize alignment first**, then **use high‑quality dense cloud**; over‑dense clouds can indeed introduce noise that later shows up as uneven cuts.

---

## 5. Where Construkted Reality Complements the Workflow  

Metashape excels at turning raw photos into a clean, editable mesh. **Construkted Reality** picks up where Metashape leaves off:

* **Asset Management** – Upload the final OBJ/FBX to Construkted’s library, tag it with capture date, GPS, and project metadata. The platform’s rich search lets teammates locate the exact model among thousands.  
* **Collaborative Workspaces** – Create a project, add the mesh as a base layer, and invite stakeholders. Annotations (e.g., “Check door clearance”) appear directly on the 3D view without altering the original file.  
* **Storytelling & Presentation** – Build a guided tour that walks a client through the edited building, highlighting the clean doorway you just cut.  
* **Versioning & Review** – Because Construkted never modifies the source asset, each edit is stored as a separate “snapshot,” allowing you to roll back if a cut was too aggressive.  

In short, Metashape gives you the **precision** you need; Construkted Reality gives you the **context** and **collaboration** you need to turn that precision into a shared decision‑making tool.

---

## 6. Best Practices for a Smooth End‑to‑End Pipeline  

1. **Capture with Overlap** – Aim for 80 % forward and 60 % side overlap; this reduces stray tie points that later require masking.  
2. **Use Ground Control Points (GCPs)** when georeferencing is critical; Metashape can ingest them directly, preserving absolute coordinates for Construkted’s globe view.  
3. **Keep a “raw” project** – Duplicate the Metashape project before you start cutting. If a later client request demands a different door size, you can revert without re‑processing the photos.  
4. **Export in a web‑friendly format** – GLTF or OBJ with low‑poly count speeds up loading in Construkted’s browser‑based viewer, keeping storage fees low.  
5. **Document the workflow** – Add a short text note in the asset’s metadata (e.g., “Door cut using Rectangle → Cut, 2025‑09‑09”). Future collaborators will appreciate the provenance.  

---

## 7. Conclusion  

The shape‑drawing and cutting tools built into Agisoft Metashape close a long‑standing gap in photogrammetry pipelines: the ability to make **precise, non‑destructive edits** without leaving the software. By following the step‑by‑step workflow above, you can turn a noisy, solid mesh into a clean, production‑ready model ready for **Construkted Reality**—the web‑based platform that lets teams store, annotate, and present those models at scale.  

When the editing happens where the data lives, you eliminate the “export‑import‑edit” loop that drains time and introduces errors. The result is faster project turn‑around, higher client confidence, and a smoother path from raw photos to collaborative 3‑D storytelling.

---

## Image Prompt Summary  

| Placeholder | Prompt for an image‑generation model |
|-------------|--------------------------------------|
| **[IMAGE 1]** | “A high‑resolution screenshot of Agisoft Metashape’s Align Photos view, showing a dense cloud of colored tie points over a building façade, with the software’s toolbar visible on the left.” |
| **[IMAGE 2]** | “Metashape mesh preview with realistic texture applied to a historic stone wall, displayed in the Model tab, with a subtle grid overlay indicating the coordinate system.” |
| **[IMAGE 3]** | “Close‑up of the Metashape Model tab toolbar, highlighting the polygon, rectangle, and circle shape‑drawing icons, with a faint glow around the active tool.” |
| **[IMAGE 4]** | “A rectangle drawn around a door opening on a 3‑D mesh in Metashape, the rectangle outlined in bright teal, the underlying mesh shown in semi‑transparent gray.” |
| **[IMAGE 5]** | “Resulting mesh after using the Cut tool: a clean, rectangular doorway opening visible in the wall, with sharp edges and no stray geometry, displayed from a slightly angled perspective.” |
| **[IMAGE 6]** | “Metashape Export Model dialog box, with checkboxes for ‘Export UV’, ‘Export Camera Positions’, and a dropdown selecting OBJ format, all set against a dark UI background.” |

---  

## References  

Agisoft Metashape Tutorial. (2025). *YouTube*. https://www.youtube.com/watch?v=1CLDeuvdD0s  

Agisoft Metashape User Manuals. (n.d.). *Agisoft*. https://www.agisoft.com/downloads/user-manuals/  

Create a clean hole in my 3D model. (2024, October 21). *Agisoft Forum*. https://www.agisoft.com/forum/index.php?topic=16735.0  

Geo‑SfM tutorial: masking photos. (n.d.). *UniSvalbard*. https://unisvalbard.github.io/Geo-SfM/content/lessons/tutorial/tutorial.html  

Metashape best settings discussion. (2024). *Reddit*. https://www.reddit.com/r/photogrammetry/comments/ws36ga/metashape_best_settings/  

Suggestions to improve model quality needed. (2017, January 26). *Agisoft Forum*. https://www.agisoft.com/forum/index.php?topic=6409.0  

Step‑by‑Step Agisoft – Metashape. (2022). *Scribd*. https://www.scribd.com/document/853571607/Step-By-Step-Agisoft-Metashape  

Tricks for optimal photogrammetry processing – Volume 1. (2025). *YouTube*. https://www.youtube.com/watch?v=JseWmlKkS2I  

---  

*All content is provided in accordance with the Construkted Reality brand guidelines and reflects the state of the platform as of September 9 2025.*