Mountebank Mocks Manager
========================

MMM is a python library, designated for automatic creation of mountebank mocks and using them in pytest tests.

Basic usage:

1. Set up your application to go to your services you want to mock via mountebank
2. Create correct proxies stubs in imposters folder
3. Write specific test you want to mock
4. Run test in proxy mode to record requests and create mocks based on these records.
5. Rerun test in mocks mode to check whether it is working and need some adjustment
