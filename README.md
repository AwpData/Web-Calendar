<h1>Directions</h1>

<li>POST to <b>.../event</b> in the following format:</li>

```
   {
        "event": "Some-Event",
        "date": "YYYY-MM-DD"
   }
```

<li> GET from <b>.../event</b> to retrieve all events you have added to the database</li>
<li> GET from <b>.../event/#</b> to retrieve event at the specified event id</li>
<li> GET from <b>.../event?starttime={date}&endtime{date}</b> to retrieve event(s) throughout the specified date range</li>
<br>
<li>DELETE from <b>.../event/#</b> to delete the event at the specified event id</li>
