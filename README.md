# internet_checker

Internet checker

## Prehistory
This program help to know when internet is available again and notify about it.

> I just want to know when the Internet will available again  
> (c) Author

Ping is too boring.

Enjoy.

## How to use
The program provides one function:  
**Check**

To use program you need pass a URL and how many retries you want to be done.

### Example 
**Check**  
`internet_checker.exe check --url http://www.google.com --retry 100`  
Checking if Internet connection available by sending 100 requests to www.google.com.  
Also check if site is available.

You also can wrap invocation with `.sh` or `.bat`. Think about it.

**Warning !**  
If set `--retry` to 0 will trigger infinity loop without end conditions. 