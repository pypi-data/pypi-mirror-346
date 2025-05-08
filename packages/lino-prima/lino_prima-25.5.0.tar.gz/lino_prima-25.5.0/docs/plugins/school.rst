.. _prima.plugins.school:

======================================
``school`` (School management)
======================================

.. module:: lino_prima.lib.school


.. contents::
  :local:

.. include:: /../docs/shared/include/tested.rst

>>> import lino
>>> lino.startup('lino_prima.projects.prima1.settings')
>>> from lino.api.doctest import *

Glossary
========

.. glossary::

  enrolment

    When a given pupil is member of a given group in a given school year.


Class reference
===============

.. class:: Group

  Django model to represent a group of pupils working together during an
  academic year (a class).

.. class:: Enrolment

  Django model to represent an enrolment of a given pupil in a given group.

Subjects, groups and courses
============================

>>> rt.show(school.Subjects)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
==== ============= ================== ===== ========== ====== ============= ==================
 ID   Designation   Designation (de)   No.   Advanced   Icon   Rating type   Image
---- ------------- ------------------ ----- ---------- ------ ------------- ------------------
 1    Science       Wissenschaften     1     Yes        🔬
 2    Art           Kunst              2     No         🎨     Smilies
 3    Music         Musik              3     No         🎜      Predicates
 4    Sport         Sport              4     No         ⛹      Predicates    26bd_soccer.png
 5    French        Französisch        5     Yes        🥐                   1f347_grapes.png
 6    Religion      Religion           6     Yes        🕊
 7    Mathematics   Mathematik         7     Yes        🖩
 8    German        Deutsch            8     Yes        🥨                   1f34e_apple.png
==== ============= ================== ===== ========== ====== ============= ==================
<BLANKLINE>

>>> rt.show(school.Groups)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
============= ================== ============== =============== ====
 Designation   Designation (de)   Grade          Academic year   ID
------------- ------------------ -------------- --------------- ----
 1A                               First grade    2024/25         1
 1B                               First grade    2024/25         7
 2A                               Second grade   2024/25         2
 2B                               Second grade   2024/25         8
 3A                               Third grade    2024/25         3
 3B                               Third grade    2024/25         9
 4A                               Fourth grade   2024/25         4
 4B                               Fourth grade   2024/25         10
 5A                               Fifth grade    2024/25         5
 5B                               Fifth grade    2024/25         11
 6A                               Sixth grade    2024/25         6
 6B                               Sixth grade    2024/25         12
============= ================== ============== =============== ====
<BLANKLINE>


Lino automatically creates a course for every subject that has "advanced"
checked and for which there is a section in the certificate template.

>>> grp = school.Group.objects.get(designation="5B")
>>> rt.show(school.CoursesByGroup, grp)
`Science <…>`__, `Art <…>`__, `Music <…>`__, `Sport <…>`__, `French <…>`__, `Religion <…>`__, `Mathematics <…>`__, `German <…>`__

>>> grp = school.Group.objects.get(designation="6A")
>>> rt.show(school.CoursesByGroup, grp)
`Science <…>`__, `French <…>`__, `Religion <…>`__, `Mathematics <…>`__, `German <…>`__


Working with scores
===================

>>> settings.SITE.site_locale
'de_BE.UTF-8'

>>> from lino_prima.lib.ratings.utils import ScoreValue, RatingCollector, format_score

>>> v1 = ScoreValue(8, 10)
>>> print(v1)
8/10
>>> print(v1.absolute)
8/10
>>> print(v1.relative)
80 %

>>> print(v1.rebase(20))
16/20

>>> v2 = ScoreValue(5, 20)
>>> print(f"{v1} + {v2} = {v1+v2}")
8/10 + 5/20 = 13/30

>>> tot = v1 + v2
>>> print(tot.relative)
43,3 %
>>> round(100*13/30, 1)
43.3
>>> import locale
>>> locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
'en_US.UTF-8'
>>> print(tot.relative)
43.3 %
>>> print(tot)
13/30

>>> print(ScoreValue(5.29, 8))
5.3/8

>>> v3 = ScoreValue(5.24, 8)
>>> print(v3)
5.2/8

>>> print(v3*3)
15.7/24


>>> tot = RatingCollector()
>>> tot.collect(8, 10)
>>> tot.collect(5, 20)
>>> print(tot)
13/30

>>> tot.ratings
[<ScoreValue(8, 10)>, <ScoreValue(5, 20)>]

>>> " + ".join(map(str, tot.ratings))
'8/10 + 5/20'


Don't read this
===============

Exploring #5835 (Link to detail of an enrolment fails for normal teachers)

This issue was fixed 20250107. Here is how to reproduce it:

- Sign in as madeleine.carbonez on ``prima1``.
- Click on "6A" in the "My groups" dashboard item.
- In the "Projects" panel of 6A, click on the first pupil (Ambroise Aelterman).
  Lino opens prima/EnrolmentsByGroup/91, which causes a BadRequest.
- There is no error when you do the same as robin.

Explanation:

When madeleine (a simple teacher) calls :meth:`obj2html` on an enrolment, Lino
uses another actor than when robin calls it because a simple teacher cannot see
all enrolments. That's normal.  Robin has access to Enrolments, Madeleine only
to EnrolmentsByGroup. But Madeleine's link then failed because EnrolmentsByGroup
requires a master instance (the group), which Lino didn't specify. Until
20250107 Lino added `mk` and `mt` for specifying the master instance only when
the target link was on the same actor as the incoming request.


>>> renderer = settings.SITE.kernel.default_renderer
>>> grp = school.Group.objects.get(designation="6A")
>>> enr = school.Enrolment.objects.get(pk=91)
>>> grp
Group #6 ('6A')
>>> enr
Enrolment #91 ('Ambroise Aelterman (6A)')
>>> ses = rt.login("robin", show_urls=True, renderer=settings.SITE.kernel.default_renderer)
>>> print(ses.permalink_uris)
None
>>> print(ses.obj2htmls(enr).replace("&quot;", "'"))
<a href="javascript:window.App.runAction({ 'actorId': 'school.Enrolments', 'an': 'detail', 'rp': null, 'status': { 'record_id': 91 } })" style="text-decoration:none">Ambroise Aelterman (6A)</a>

>>> ses = rt.login("madeleine.carbonez", show_urls=True, renderer=settings.SITE.kernel.default_renderer)
>>> ar = projects.PupilsAndProjectsByGroup.create_request(master_instance=grp, renderer=renderer, user=ses.get_user())
>>> print(ar.obj2url(enr))  #doctest: +NORMALIZE_WHITESPACE
javascript:window.App.runAction({ "actorId":
"projects.PupilsAndProjectsByGroup", "an": "detail", "rp": null, "status": {
"base_params": { "mk": 6, "mt": 9 }, "record_id": 91 } })

Note: After fixing the bug, I changed PupilsAndProjectsByGroup to inherif from
EnrolmentsByGroup rather than VirtualTable, which would have
