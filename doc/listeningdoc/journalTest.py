# output journal entries for apache

from systemd import journal

j = journal.Reader()
j.this_boot()
j.log_level(journal.LOG_INFO)
j.add_match(_SYSTEMD_UNIT="bluetooth.service")
# j.add_match(_SYSTEMD_PID="1")

for entry in j:
    print(entry['MESSAGE'])
    # print(entry)
    # print(entry['PID'])
    