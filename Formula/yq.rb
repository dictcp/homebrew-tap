class Yq < Formula
  include Language::Python::Virtualenv

  desc "Command-line YAML processor - jq wrapper for YAML documents"
  homepage "https://yq.readthedocs.io/"
  url "https://github.com/kislyuk/yq/archive/v2.3.4.tar.gz"
  sha256 "e8265dfc11a1158215b4b1986c315b64a481d856d057f475b541c1edd62aa824"
  head "https://github.com/kislyuk/yq", :branch => "master"

  depends_on :python if MacOS.version <= :lion

  def install
    venv = virtualenv_create(libexec)
    system libexec/"bin/pip", "install", "-v", "--no-binary", ":all:",
                              "--ignore-installed", buildpath
    system libexec/"bin/pip", "uninstall", "-y", "yq"
    venv.pip_install_and_link buildpath
  end

  test do
    assert_match "options", shell_output("#{bin}/yq --help")
  end
end

