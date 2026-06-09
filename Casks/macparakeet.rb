cask "macparakeet" do
  version "0.6.4"
  sha256 "02820e86755c6f2ccdf0a2ee7f234520a25113ae27db48d3c667a96a27919cd8"

  url "https://github.com/moona3k/macparakeet/releases/download/v#{version}/MacParakeet.dmg"
  name "MacParakeet"
  desc "Fast voice app for Mac with fully local speech and optional AI"
  homepage "https://macparakeet.com"

  livecheck do
    url :url
    strategy :github_latest
  end

  auto_updates true
  depends_on macos: :sonoma

  app "MacParakeet.app"

  zap trash: [
    "~/Library/Application Support/MacParakeet",
    "~/Library/Preferences/com.macparakeet.plist",
  ]
end
