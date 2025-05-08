# OH Sched

Assigns TA offers hours to their preferences, which are obtained via [google forms](https://docs.google.com/forms/d/1Wm82XnLux83t3pZvLMcAhuiJZKEEsbs4kcqXnotI5bs/template/preview).  
- support for multiple TAs per Office hours slot
- allows instructor to "nudge" preferences (e.g. preferring office hours slots just before HW deadline)
- exports final schedule to ics file (compatiable with most calendar apps)

# Installation
```bash
python3 -m pip install oh_sched
```

(Windows users swap `python` for `python3`)

# Usage
- Ask all TAs to fill out a [google form](https://docs.google.com/forms/d/1Wm82XnLux83t3pZvLMcAhuiJZKEEsbs4kcqXnotI5bs/template/preview) with their office hours preferences
  - (please modify this template as needed, see [Formatting Office Hours Time](#formatting-office-hours-time))
- Download the csv of responses
  - see [test/oh_pref.csv](test/oh_prefs.csv) for example 
- Run the following command on the downloaded csv file
```bash
python3 -m oh_sched oh_pref.csv
```
- The schedule will be printed to the command line (see [test/ex_output.txt](test/ex_output.txt) for example) and written to `oh.ics` which can be imported into most calendar apps (e.g. Google, Outlook, Apple)
- The default configuration file, `config.yaml` will also be written locally.  Please modify it as needed (see [configuration section](#configuration)) and re-run to account for your adjustments:
```bash
python3 -m oh_sched oh_pref.csv -c config.yaml
```

# Matching

The table below gives the preferences of two TAs for four office hours slots.  Larger values are preferred and empty cells indicate incompatibility.  How can we assign each TA `oh_per_ta=2` office hours slots to optimize the sum of assigned preferences?

|     | OH0 | OH1 | OH2 | OH3 |
|-----|-----|-----|-----|-----|
| TA0 | 4   | 3   |     |     |
| TA1 |     | 3   | 4   | 1   |

By inspection, in this simple case it is best if 
- TA0 is assigned OH0 and OH1
- TA1 is assigned OH1 and OH2

This yields a sum of assigned preferences of 4 + 3 + 3 + 4 = 14

Programmatically, when `oh_per_ta=1`, one may use [scipy.optimize.linear_sum_assignment()](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linear_sum_assignment.html), a Hungarian Algorithm variant, to match TAs to office hours.  Please see  [match()](oh_sched/match.py)) for full detail, but briefly:
- To solve for `oh_per_ta > 1` we use a greedy extension which iteratively assigns each TA to the available office hours slot which best suits their preferences while excluding previous OH assignments
- Because each office hours slot may be repeated, each column of the matrix above is repeated per its remaining availability.

# Configuration

See [test/config.yaml](test/config.yaml) for example:

- `oh_per_ta`: how many office hours slots assigned to each TA (default: 1)
- `max_ta_per_oh`: maximum number of TAs which may be assigned to any office hours slot.  By default, no maximum is imposed and all TAs may share a single office hours slot.
- `f_out`: name of the output ics file of your calendar (by default no ics file is written)
- `verbose`: toggles command line output (default: true)
- `date_start`: the starting date (inclusive) for office hours in the output ics calendar (default: today)
  - any format readable by [pd.to_datetime()](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html) is fine
- `date_end`: the ending date (inclusive) for office hours in the output ics calendar (default: 6 days from `date_start`, so output is one full week)
- `scale_dict`: allows the user to apply a multiplier to TA preferences to suit course needs.  For example, if more OH coverage is helpful on Thursday and Friday one could write:
```yaml
    scale_dict:
      Thu: 1.1
      Fri: 1.2
```
which multiplies preferences on slots which match the regex string "Thu" by 1.1 and "Fri" by 1.2.  Please be mindful that the scaling magnitudes aren't so severe that they violate initial TA preferences.  Please check to ensure the output includes the scaling you intend by checking the "Scaling office hours preferences:" section of the output (see [test/ex_output.txt](test/ex_output.txt) for example).

# Formatting office Hours Time

Office hours take place weekly during a timeslot on one day of the week.  Here are two valid examples:
```
    Mondays 3PM-4PM Cargill 097
    Tue 11:15am-1 Pm Virtual
```
The output `.ics` calendar will include all non-time related string input in the calendar event.  For example, the examples above might produce calendar events:
```
    Cargill 097: ta0, ta1
    Virtual: ta2, ta3, ta4
```
where the ta lists are determined by the matching method described above.  Following these examples is sufficient, here are the gory parsing details:

- The day is given as case-insensitive 3-letter abbreviation or full name (e.g. "thu" or "Thursday").  Note that this must be a separate word in the input (i.e. "Mon9:00AM-10:00AM" is invalid, needs space after "Mon").
- Start and end times for office hours are separated by the unique appearance of '-'.
- see `OfficeHours.__init__()` and `parse_day()` / `parse_time()` in [calendr.py](oh_sched/calendr.py) for full details.

# Percentage Max

To quantify the quality of the matching, we compute a percentage maximum score for every TA.  Consider the following toy example:

|     | OH0 | OH1 | OH2 | OH3 |
|-----|-----|-----|-----|-----|
| TA0 | 4   | 3   |     |     |
| TA1 |     | 3   | 4   | 1   |

Let us assume that we're assigning two office hours slots per TA (i.e. `oh_per_ta=2`).  In this case, the maximum preference score for TA1's two OH slots is 7 (assigning them OH1 and OH2).  If TA1 was assigned OH2 and OH3 then the schedule achieved a score of only 5.  In this case TA1's percentage max is $5/7\approx.71$.  

The TA with the smallest percentage max score has the least favorable schedule, as compared to their own preferences.  Examining the minimum and mean percentage max score, printed as output, gives a sense of how favorable the matching is for TAs.

# Email Comparison

The software will take the latest TA preference, allowing TAs to update their preferences as desired.  One challenge here is that a typo on entering their email a second (or first) time would have the software treat each entry as belonging to a unique TA.  To mitigate this, we throw a warning when two emails are sufficiently similar (Levenshtein distance of 2 or less).  Other than warning, no adjustment is made by the software.  Should you receive this warning, please manually edit the input CSV and re-run as needed.