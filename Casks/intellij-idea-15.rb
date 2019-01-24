cask 'intellij-idea-15' do
  version '15.0.6'
  sha256 '277203d7cb0912a81422f4469c838c986be9b15061d12698184026a490546f50'

  url "https://download.jetbrains.com/idea/ideaIU-#{version}-custom-jdk-bundled.dmg"
  name 'IntelliJ IDEA'
  homepage 'https://www.jetbrains.com/idea/'

  conflicts_with cask: ['intellij-idea', 'intellij-idea-eap']

  app 'IntelliJ IDEA 15.app'

  zap delete: [
                "~/.IntelliJIdea#{version.major}",
                "~/Library/Caches/IntelliJIdea#{version.major}",
                "~/Library/Logs/IntelliJIdea#{version.major}",
                "~/Library/Application Support/IntelliJIdea#{version.major}",
                "~/Library/Preferences/IntelliJIdea#{version.major}",
                '~/Library/Preferences/com.jetbrains.intellij.plist',
              ]
end
