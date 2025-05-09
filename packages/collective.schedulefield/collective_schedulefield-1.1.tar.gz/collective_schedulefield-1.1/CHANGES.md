# Changelog

## 1.1 (2025-05-08)

- Update locales https://github.com/IMIO/collective.schedulefield/issues/3
  [remdub]

- Add test environment using pytest, with test coverage reaching 80% https://github.com/IMIO/collective.schedulefield/issues/2
  [remdub]

- Fix MultiSchedule viewlet https://github.com/IMIO/collective.schedulefield/issues/4
  [remdub]

- Upgrade dev environment to Plone 6.1-latest
  [remdub]


## 1.0a3 (2023-01-12)

- MANIFEST / release fix
  [laulaz]


## 1.0a2 (2023-01-12)

- Drop support for Plone 4 & Plone 5
  [laulaz]

- Fix AttributeError traceback when accessing subforms
  [laulaz]


## 1.0a1 (2022-12-13)

- Add basic serializers / deserializers
  [laulaz]

- Display schedule viewlets only on views (not on folder_contents, cropping, etc.)
  [laulaz]

- Fix error when validating an empty value for a schedule
  [laulaz]

- Add missing key_type/value_type for Schedule field. This is needed (at least)
  to export types schemas information
  [laulaz]

- Fix python3 compatibility : Use @implementer instead of implements
  [boulch]

- Handle multi schedules and exceptional closures
  [fbruynbroeck]


## 0.6.1 (2018-10-15)

- Do not display comment if empty.
  [bsuttor]


## 0.6 (2018-04-23)

- Also view schedule if only comment is set.
  [bsuttor]

- Added missing z3c.form meta.zcml.
  [sgeulette]


## 0.5 (2017-04-27)

- Bugfix: get json schedule.
  [bsuttor]


## 0.4 (2017-04-25)

- Bugfix: do not try to load json value if there is no values.
  [bsuttor]


## 0.3 (2017-03-01)

- Do not render the viewlet if there is no values
  [mpeeters]


## 0.2 (2016-07-14)

- Add the ScheduledContent behavior
  [mpeeters]

- Add a comment field for each schedule day
  [mpeeters]


## 0.1 (2014-08-26)

 - Initial release
