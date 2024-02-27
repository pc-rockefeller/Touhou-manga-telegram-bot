package myjar

import (
	"fmt"
	"net/http"
	"net/url"
)

type Myjar struct {
	Jar map[string][]*http.Cookie
}

func (p *Myjar) SetCookies(u *url.URL, cookies []*http.Cookie) {
	fmt.Printf("The URL is : %s\n", u.String())
	fmt.Printf("The cookie being set is : %s\n", cookies)
	p.Jar[u.Host] = cookies
}

func (p *Myjar) Cookies(u *url.URL) []*http.Cookie {
	fmt.Printf("The URL is : %s\n", u.String())
	fmt.Printf("Cookie being returned is : %s\n", p.Jar[u.Host])
	return p.Jar[u.Host]
}
