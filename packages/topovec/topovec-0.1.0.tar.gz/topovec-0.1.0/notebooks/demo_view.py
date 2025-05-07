import marimo

__generated_with = "0.11.20"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import topovec as tv
    return mo, np, tv


@app.cell
def _(tv):
    # Settings.
    SRC_FOLDER = './files/' # Location of data files.
    FIGSIZE = 512 # Image size.

    # Name of datafile.
    srcname = 'CCW_800_opposite_mix.npz'

    # Load data.
    images, system, settings = tv.core.load_lcsim_npz(f"{SRC_FOLDER}/{srcname}")

    # Prepare scene.
    ic = tv.mgl.render_prepare(
        scenecls = 'Isolines',
        system = system,
        imgsize = FIGSIZE,
    )
    return FIGSIZE, SRC_FOLDER, ic, images, settings, srcname, system


@app.cell
def _(mo, np, system):
    def to_deg(x): return float(x/np.pi*180) 
    def to_rad(x): return x/180*np.pi

    # UI definition
    ui_scale = mo.ui.number(label="Scale", start=1, stop=1000, step=1, value=float(system.size[0]/4))
    ui_theta = mo.ui.number(label="Camera azimuthal angle", start=0, stop=360, step=1, value=0.)
    ui_phi = mo.ui.number(label="Camera polar angle", start=0, stop=180, step=1, value=0.)
    ui_alpha = mo.ui.number(label="Camera up angle", start=0, stop=360, step=1, value=0.)

    ui_look_at = mo.ui.array([
        mo.ui.number(start=0, stop=float(system.size[n]), step=1, value=float(system.size[n]/2))
    for n in range(3)], label="Look at")
    return to_deg, to_rad, ui_alpha, ui_look_at, ui_phi, ui_scale, ui_theta


@app.cell
def _(ui_alpha, ui_look_at, ui_phi, ui_scale, ui_theta):
    # Show UI
    ui_scale, ui_theta, ui_phi, ui_alpha, ui_look_at
    return


@app.cell
def _(
    ic,
    images,
    to_rad,
    tv,
    ui_alpha,
    ui_look_at,
    ui_phi,
    ui_scale,
    ui_theta,
):
    # Select data to plot.
    director = images[0] 
    ic.upload(director) 

    # Setup camera.
    ic.scene.set_camera(tv.mgl.Camera.from_angles(
        theta=to_rad(ui_theta.value),
        phi=to_rad(ui_phi.value),
        alpha=to_rad(ui_alpha.value),
        scale=ui_scale.value,
        perspective=True,
        look_at=ui_look_at.value,
    ))

    # Run render.
    ic.save()
    return (director,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
