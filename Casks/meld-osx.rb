cask "meld-osx" do
  version "3.21.0"
  sha256 "50a4a45b3b7f44910c1a4c782c044579bc9dd09432c5e0a965dbeb973bbc767e"

  # Releases use an 'osx-N' tag scheme independent of the semantic version;
  # update the tag below whenever a new release is published.
  url "https://github.com/yousseb/meld/releases/download/osx-19/meldmerge.dmg"
  name "Meld"
  desc "Visual diff and merge tool"
  homepage "https://yousseb.github.io/meld/"

  livecheck do
    url "https://github.com/yousseb/meld/releases/latest"
    regex(/OSX[^(]*?([\d]+\.[\d]+\.[\d]+)/i)
  end

  app "Meld.app"
end
