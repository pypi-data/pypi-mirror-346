class Trmd < Formula
  include Language::Python::Virtualenv

  desc "Translate Markdown using OpenAI"
  homepage "https://github.com/rioriost/homebrew-trmd/"
  url "https://files.pythonhosted.org/packages/91/81/2727f274169ee823b9a71cf667ea411d03f15b1da7fa542a4b1a08e3a4fe/trmd-0.1.4.tar.gz"
  sha256 "cf04c4255ffa35e6ea46bce9f5744acdf28ad7b9cff35333e0aceb23b4e95151"
  license "MIT"

  depends_on "python@3.13"

  def install
    virtualenv_install_with_resources
    system libexec/"bin/python", "-m", "pip", "install", "openai"
  end

  test do
    system "#{bin}/trmd", "--help"
  end
end
