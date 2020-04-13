  
cask 'kubenav' do
  version "1.13.0"
  sha256 "f7685ca9162f42f43076d4c9b495f96c1fc4b3b2fdbe094c06bc941900eafea1"

  url "https://github.com/kubenav/kubenav/releases/download/1.3.0/kubenav-1.3.0-darwin-amd64.dmg"
  name 'kubenav'
  homepage 'https://kubenav.io/'

  app 'kubenav.app'
end
