REM to install: winget upgrade Microsoft.devtunnel
devtunnel user login

REM Tunnel port 8080 (elasticsearch) in new window with anonymous access
start "Elasticsearch Tunnel" devtunnel host -p 8080 --allow-anonymous

echo Elasticsearch tunnel started with anonymous access.