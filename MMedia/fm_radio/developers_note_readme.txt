Important:
The RDSDecoder module tries to read the radio device in a thread and may block while some
other function of the FMRadio module tries to read or write the device.
Therefore all calls to the device must become thread safe
