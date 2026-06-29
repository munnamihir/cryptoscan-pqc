using System.Security.Cryptography;

public class LegacyCrypto {
    public RSA NewKey() => RSA.Create(2048);
    public void Hash() { using var md5 = MD5.Create(); }
    public void Cipher() { using var des = TripleDES.Create(); }
}
