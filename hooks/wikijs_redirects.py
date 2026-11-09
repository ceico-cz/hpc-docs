"""Keep old Wiki.js URLs working: /en/<path> and /home redirect to the new pages."""
import os

# Wiki.js page paths that changed during the migration, served at both /<path> and /en/<path>.
WIKIJS_PATHS = {
    "acknowledgement_template": "systems/phoebe/acknowledgement.md",
    "admin-stuff": "admin/index.md",
    "admin-stuff/Advantech_USB-5855_in_Ubuntu_23": "admin/blog/posts/2024-02-14-advantech-usb-5855.md",
    "admin-stuff/Build_cosmosis_with_Python27": "software/cosmosis-py27.md",
    "admin-stuff/Slurm_accoounting_admin_notes": "admin/slurm-accounting.md",
    "admin-stuff/Slurm_admin_snippets": "admin/slurm-snippets.md",
    "app/pyoperon": "software/pyoperon.md",
    "conda/cupy": "software/cupy.md",
    "getting-a-user-account/create-ssh-keypair-nix": "getting-started/ssh-key.md",
    "getting-a-user-account/create-ssh-keypair-win": "getting-started/ssh-key.md",
    "getting-there/desktop": "getting-started/ondemand/desktop.md",
    "getting-there/getting-a-user-account": "getting-started/account.md",
    "getting-there/ssh": "getting-started/ssh.md",
    "getting-there/ssh/linux": "getting-started/ssh.md",
    "getting-there/ssh/mac": "getting-started/ssh.md",
    "getting-there/ssh/windows": "getting-started/ssh.md",
    "getting-there/using-jupyterLab-at-ondemand": "getting-started/ondemand/jupyterlab.md",
    "hardware": "systems/phoebe/infrastructure.md",
    "interactive_cli_job": "compute/interactive.md",
    "koios": "systems/koios/index.md",
    "koios/hw": "systems/koios/infrastructure.md",
    "koios/hw/p100": "systems/koios/infrastructure.md",
    "koios/hw/Xeon_Gold_6130": "systems/koios/infrastructure.md",
    "mesa-mesa_sdk": "software/mesa.md",
    "metacentrum/hq_at_metacentrum": "systems/metacentrum/hyperqueue.md",
    "slurm/interactive_slurm_cli_session": "compute/interactive.md",
    "slurm/slurm_jobs_troubleshooting": "compute/troubleshooting.md",
    "submit-job": "compute/batch-jobs.md",
    "useful": "tips/index.md",
    "useful/bash_tweaks": "tips/bash-tweaks.md",
    "useful/get_public_ip": "tips/bash-tweaks.md",
    "useful/module_use": "software/modules.md",
    "useful/poor_mans_vpn_ssh": "getting-started/socks-proxy.md",
    "useful/python-uv": "software/python-uv.md",
    "useful/screen_config": "tips/screen.md",
    "useful/sshfs": "getting-started/sshfs.md",
    "useful/sshfs/sshfs_linux": "getting-started/sshfs.md",
    "useful/sshfs/sshfs_macos": "getting-started/sshfs.md",
    "useful/unpack_rpm": "software/unpack-rpm.md",
    "wolfram/main_page": "software/mathematica/index.md",
}


def on_config(config):
    maps = config.plugins["redirects"].config["redirect_maps"]
    docs = config["docs_dir"]
    excluded = config["exclude_docs"]  # pages kept in the repo but not published
    for old, new in WIKIJS_PATHS.items():
        maps.setdefault(f"{old}.md", new)
        maps.setdefault(f"en/{old}.md", new)
    for root, _, files in os.walk(docs):
        for f in files:
            if not f.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, f), docs).replace(os.sep, "/")
            if excluded and excluded.match_file(rel):
                continue
            if rel == "index.md":
                maps.setdefault("home.md", rel)
                maps.setdefault("en/home.md", rel)
                maps.setdefault("en/index.md", rel)
            else:
                maps.setdefault(f"en/{rel}", rel)
    return config
