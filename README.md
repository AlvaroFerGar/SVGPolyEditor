# ⭔ SVG Polygon Editor ⭔

A basic editor for polygons in SVG format, designed for a side project. It allows you to load SVG files, modify the polygon's points, and save the changes to a new SVG file.
<div id="header" align="center">
  <img src="images/app.png" width="400"/>
</div>


## Expected Input Format
SVG files should follow this format:
```xml
<svg xmlns='http://www.w3.org/2000/svg' viewBox='-60 -50 120 120'>
  <!--
  <svg xmlns='http://www.w3.org/2000/svg' viewBox='xmin ymin width height'>
  -->
  <polygon points='43.64,31.46 31.94,42.69 ...' fill='#185452' stroke='black' stroke-width='1'/>
  <!--
  <polygon points='x1,y1 x2,y2 ...' fill='color_bckg' stroke='color_border' stroke-width='stroke_width'/>
  -->
</svg>
```

## How to Use
1. **Load an SVG File** : Click the "Load SVG" button and select a valid file.
2. **Modify the Points** :
   - **Double click**  on the canvas to add a point.
   - **Drag a point**  to move it.
3. **Center the Polygon** : Use the "Center Points" button to move the polygon to the center of the canvas.
4. **Change Colors** : Edit the "Fill Color" and "Stroke Color" values and press "Apply Colors."
5. **Save the SVG File** : Click "Save SVG" and choose a location to save the edited file.

## Limitations
- Adding new points may be a little buggy 🐞