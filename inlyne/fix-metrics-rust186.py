#!/usr/bin/env python3
"""Fix metrics crate for Rust 1.86+ (rust-lang/rust#141402)"""
import hashlib
import json
import pathlib

mod_rs = pathlib.Path("vendor/metrics/src/recorder/mod.rs")
text = mod_rs.read_text()

old_sig = "fn new(recorder: &'a dyn Recorder) -> Self {"
new_sig = "fn new(recorder: &'a (dyn Recorder + 'a)) -> Self {"

old_body = "let recorder_ptr = unsafe { NonNull::new_unchecked(recorder as *const _ as *mut _) };"
new_body = """let recorder_ptr = unsafe {
            std::mem::transmute::<*const (dyn Recorder + 'a), *mut (dyn Recorder + 'static)>(
                recorder as &'a (dyn Recorder + 'a),
            )
        };
        let recorder_ptr = unsafe { NonNull::new_unchecked(recorder_ptr) };"""

text = text.replace(old_sig, new_sig)
text = text.replace(old_body, new_body)
mod_rs.write_text(text)

# Update cargo checksum
new_hash = hashlib.sha256(text.encode()).hexdigest()
cksum_path = pathlib.Path("vendor/metrics/.cargo-checksum.json")
cksum = json.loads(cksum_path.read_text())
cksum["files"]["src/recorder/mod.rs"] = new_hash
cksum_path.write_text(json.dumps(cksum))
