$falcon/investigate:aidmaster()
| event_platform=/(^(Win|Mac|Lin)$)/
| test(Time > start())
| test(Time < end())
| regex(regex="(?<VersionFamily>\d+\.\d+)\.(?<build>\d+)", field=AgentVersion)
| format(format="%s%s%s", field=[event_platform, VersionFamily, build], as=KEY)
| match(file="falcon/investigate/sensors_support_info.csv", field=KEY, strict=true)
| AAA := parseTimestamp("M/d/yy", timezone="UTC", field=SUPPORT_ENDS)
| currentTime := now()
| timeDiff := (AAA-currentTime)/1000
| case {
    timeDiff < 0
      | SupportStatus := "Unsupported";
    timeDiff > 0 AND timeDiff < 7776000
      |  SupportStatus := "Old";
    timeDiff > 7776000
      | SupportStatus := "Good";
}
| SupportStatus != "Good"
| groupBy([ComputerName, aid], function=collect(SupportStatus), limit=max)
