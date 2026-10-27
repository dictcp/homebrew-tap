cask "macparakeet" do
  version "0.8.10"
  sha256 "a80a4d401ad538dc37c4b2c826b47077064b7f085f3f24cbda481d8219634090"

  url "https://github.com/moona3k/macparakeet/releases/download/v#{version}/MacParakeet.dmg"
  name "MacParakeet"
  desc "Fast voice app for Mac with fully local speech and optional AI"
  homepage "https://macparakeet.com"

  livecheck do
    url :url
    strategy :github_latest
  end

  auto_updates true
  depends_on macos: "14.2"
  depends_on arch: :arm64

  app "MacParakeet.app"

  zap trash: [
    "~/Library/Application Support/MacParakeet",
    "~/Library/Preferences/com.macparakeet.plist",
  ]
end
