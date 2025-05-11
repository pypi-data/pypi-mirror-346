use std::env;
use std::fs;
use std::io::Write;
use std::path::PathBuf;
use std::process::Command;

use pyo3::prelude::*;

const FFMPEG_BYTES: &[u8] = include_bytes!("../bin/ffmpeg");

#[pyfunction]
fn compress_video(input_path: &str, output_path: &str) -> PyResult<()> {
    // Prepare a temp directory to dump ffmpeg binary
    let temp_dir = env::temp_dir().join("kideo_ffmpeg");
    let ffmpeg_path = temp_dir.join("ffmpeg");

    if !ffmpeg_path.exists() {
        fs::create_dir_all(&temp_dir).map_err(|e| {
            pyo3::exceptions::PyIOError::new_err(format!("Failed to create temp dir: {}", e))
        })?;
        let mut file = fs::File::create(&ffmpeg_path).map_err(|e| {
            pyo3::exceptions::PyIOError::new_err(format!("Failed to write ffmpeg binary: {}", e))
        })?;
        file.write_all(FFMPEG_BYTES).map_err(|e| {
            pyo3::exceptions::PyIOError::new_err(format!("Failed to write ffmpeg data: {}", e))
        })?;
        #[cfg(unix)]
        {
            use std::os::unix::fs::PermissionsExt;
            let mut perms = file.metadata()?.permissions();
            perms.set_mode(0o755); // make it executable
            fs::set_permissions(&ffmpeg_path, perms)?;
        }
    }

    let status = Command::new(&ffmpeg_path)
        .args([
            "-i", input_path,
            "-vf", "scale=-2:240,fps=15",
            "-c:v", "libvpx-vp9",
            "-crf", "28",
            "-b:v", "0",
            "-c:a", "libopus",
            output_path,
        ])
        .status()
        .map_err(|e| {
            pyo3::exceptions::PyRuntimeError::new_err(format!("Failed to execute FFmpeg: {}", e))
        })?;

    if status.success() {
        Ok(())
    } else {
        Err(pyo3::exceptions::PyRuntimeError::new_err("FFmpeg compression failed"))
    }
}

#[pymodule]
fn kideo(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(compress_video, m)?)?;
    Ok(())
}
