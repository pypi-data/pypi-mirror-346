from atelier.invlib import setup_from_tasks

ns = setup_from_tasks(
    globals(),
    "lino_prima",
    languages="en de fr".split(),
    # tolerate_sphinx_warnings=True,
    locale_dir='lino_prima/lib/prima/locale',
    revision_control_system='git',
    cleanable_files=['docs/api/lino_prima.*'],
    # demo_prep_command="manage.py prep -v3 --noinput --traceback",
    demo_projects=['lino_prima.projects.prima1'])
