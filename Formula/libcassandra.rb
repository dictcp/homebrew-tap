class Libcassandra < Formula
  version "2.4.1"
  desc "C and C++ client library to the cassandra server"
  homepage "htt:p://libmemcached.org"
  url "https://github.com/datastax/cpp-driver/archive/#{version}.tar.gz"
  sha256 "66022fbf932fc0a41cb2e5786046e74b6650da0e78927cdcf111867810a0c299"
  revision 1

  depends_on "cmake" => :build
  depends_on "openssl"
  depends_on "libuv"

  def install
    args = ["-DOPENSSL_INCLUDE_DIR=#{Formula["openssl"].opt_include}", "-DCMAKE_INSTALL_PREFIX=#{prefix}"]

    system "cmake", *args, "."
    system "make", "install"
  end
end
