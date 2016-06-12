cask 'meld-osx' do
  version "3.16.0"
  sha256 "324e096e0253e8ad4237f64a90cdda200fe427db8cf7ebc78143fc98e2d33ebc"

  url "https://github.com/yousseb/meld/releases/download/osx-9/meldmerge.dmg"
  name 'Meld'
  homepage 'https://yousseb.github.io/meld/'
  license 'gpl'

  app 'Meld.app'

end
