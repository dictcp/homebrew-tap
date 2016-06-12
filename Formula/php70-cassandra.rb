require File.expand_path("../../Abstract/abstract-php-extension", __FILE__)

class Php70Cassandra < AbstractPhp70Extension
  init
  version "1.1.0"
  desc "DataStax PHP Driver for Apache Cassandra"
  homepage "https://pecl.php.net/package/cassandra"
  url "https://pecl.php.net/get/cassandra-#{version}.tgz"
  sha256 "e9f196bad4d2d64a0ef5be113d855db85c662c36ae7a23644c2573adb01b854a"

  depends_on "pkg-config" => :build
  depends_on "libcassandra"
  depends_on "libuv"
  depends_on "gmp"

  def install
    Dir.chdir "cassandra-#{version}" unless build.head?

    ENV.universal_binary if build.universal?

    safe_phpize

    system "./configure", "--prefix=#{prefix}",
                          phpconfig
    system "make"
    prefix.install "modules/cassandra.so"
    write_config_file if build.with? "config-file"
  end
end
