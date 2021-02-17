# Yearly Goal Sheet

Yearly Goal Sheet is a short python script that generates an A4 size calendar image for a given year. It's intended to be used for following a single goal throughout the year by checking off each day.

## How to Run

The main code was developed in a notebook but it's also exported & adjusted into a script.

```terminal
python sheet_generator.py -t "This is my Goal"
```
It also works for couples who want to work on the same goal.

```terminal
python sheet_generator.py -t "This is our Goal" -y 2024 -p 2 -i "TL" -c "#7e3a91"
```

## Parameters

```python
-t, --title,    Title of the Goal,                                required=True,                 type=str
-y, --year,     Year of the Goal,                                 default=datetime.today().year, type=int
-p, --people,   Number of People (1 or 2),                        default=1,                     type=int
-i, --initials, Initials of the two people. String of length 2.,  default=None,                  type=str
-c, --color,    Color of the Sheet (Dark),                        default='#2c5c74',             type=str
```

## Example 1

A single person wants to follow his/her's goal.

![Image from Images](https://github.com/orion512/yearly_goal_sheet/blob/main/images/example_goals_calendar.png)

## Example 2

A couple Tom and Lisa want to follow their goal.

![Image of Yaktocat](https://github.com/orion512/yearly_goal_sheet/blob/main/images/example_couple_goals_calendar.png)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)