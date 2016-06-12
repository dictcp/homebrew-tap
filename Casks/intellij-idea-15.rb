cask 'intellij-idea' do
  version '15.0.6'
  sha256 '3bb97dcb03d1302dcea28adb7b8ffd959d65eb87aa6715d4dace62902f9f5e73'

  url "https://download.jetbrains.com/idea/ideaIU-#{version}.dmg"
  name 'IntelliJ IDEA'
  homepage 'https://www.jetbrains.com/idea/'
  license :commercial

  conflicts_with cask: 'intellij-idea'
  conflicts_with cask: 'intellij-idea-eap'

  app 'IntelliJ IDEA.app'

  uninstall delete: '/usr/local/bin/idea'

  zap delete: [
                "~/Library/Caches/IntelliJIdea#{version.major_minor}",
                "~/Library/Logs/IntelliJIdea#{version.major_minor}",
                "~/Library/Application Support/IntelliJIdea#{version.major_minor}",
                "~/Library/Preferences/IntelliJIdea#{version.major_minor}",
              ]
end
