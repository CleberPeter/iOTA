#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cstddef>

#include <mbedtls/ecdsa.h>
#include <mbedtls/sha256.h>
#include <mbedtls/entropy.h>
#include <mbedtls/ctr_drbg.h>
#include <mbedtls/ecdh.h>
#include <mbedtls/pk.h>

using namespace std;

#define CURVE MBEDTLS_ECP_DP_SECP256K1

#define RSA

#if defined(RSA)

int main(int argc, char *argv[])
{
    mbedtls_pk_context rsa;
    int ret;

    char* private_key_project_str = "308204a90201000282010100879f57013dfce149cebc460171d5d35db0e76559af2d60736e10aecb6a9c9d1e4afed4bb5817faf29b321d488a3cac43be13a3ffe6d9270a208b667e58fb5e910977da79a40e9f19d0c111d140541df511aef5bfaee0daca6118403fea0c8aaff21a38fc5412cbec7886355a4160775237716d6cfb2ee5aa53e29b19856a1471ea63921dcef38fdf38f8a8667ded4420a2b737e776f85f417a251090d9c7c14a39dcdb1464d0b6c6214c891b4521503925e3a00a7ba7b00ce767e6835cc08ddc1b116ca73f7ff0c08cb9419e06b79911b587d240c613754529f21f0b4b231012ef80f2973a4d8c50b5c0ebea1cff19fa49ac1fd200ec254b4001e8ecbe0fa6730203010001028201000f886e5c940eec769998f2a3a3b80bb745559b44044e3c27bc4968db9f6044967d9c661cf6dff83be50e7e501a950c5dcddd4e01371d53dd5310e432405ab9dffea79d7c25100fa4d345e9967fb9a29cb8e3c2fdab37d197303ba8d0292c3a8e203a64a071b89d667dff5108ff47df22a97af23f731d51ec7a6c0a18d23150825b3fb49375799b99df33e0c0077b856eaa8747a977a7562de12cbf415a18a25746a09e87a3361056f5bebc41af120221f2d1bfc5498f02768052b98210fe14a45995a0cb68af179a70f2dcea0087e0b5b3e5288abb1cfea2cfa506f9430fbace9ef0b43057995bd9c02288f6bd749e53b90d453142f77c1f29291322ca45ca110281890089359a2eff82685b69f186af70826dfc03f0490b9beb75b944a29f2b9c10a57e79a3bea7d6c3937e9debb625b7963ce413f8411229de2729e1e03cd19ded0b4ae1d62c92b3271a0bc162ba33901d25a32f2a06f007fc592e32516369cfe3bd5b499590769be923050aa9d790784178743b61d50d329b8ea3579753c26f2131c908c629c6269e6c6f027900fd0a02dcd1a6c7b66d39b28f8a6331fa6987c912c79aa3ce2b0df56136af9c916c2788c12a6a7a4d3cedf2e8e04f9e39e96c8e7645de4a767065d568c9f8b6bc366df246f20c4fba6da0d434e6c7a2a355e58179660039194b3fe8b7e97be55ef7df38ecee5df5545fefe2d35531ea12c81b9bd24d35303d0281886f79822bdee11761f5a009f9ed61ba73becb70bd22cf5914cd8385e80b62a6e22b777285b001b38a724937f24ac69feff99d7f587f7582c20f467c831d58a20d13904b2460b34b00f3fbff25b75746e5de82b9a2380ab875c4e1c4f009bb90736344455b67ee30ca7ed060577aac4e6db87512802776a49b66a586a2786132ae8f17588729871ab7027900b9f92ca76cf2fe1f66e19c0a0174ec5b964a350f3762c1779a8f34c49133ba87eb0c9767192c8edccba63afccb37d91bc9227f06104dd33e7f5768e50e645cb1b1f356b8abd73e95cf5300042d85965423a27d6962fd50f9f523708012fb7b5634297ca62e7f21fb345393cb2cf77588fe47c45b696169250281884b9e3dbbda0c65a8dee150744edcd71b387deda3a181456d0508019a1c8ffda77097508763760168655015982bec4b2ed67a4c04cc006fe6beaf8f306042d82e17c0cb9649326ad246d4d67db7de56893ab8d2788dbcceaeb4434f8ea09fd4aefc651c41c6045f8a0444ad7445b4d1286b82564150d360c4d1ad1f25a41b83390594ecdbd4edd158";
    size_t private_key_project_size = strlen(private_key_project_str)/2;
    unsigned char private_key_project[private_key_project_size];

    for (size_t idx = 0; idx < private_key_project_size; idx++) {
        sscanf(&private_key_project_str[idx*2], "%2hhx", &private_key_project[idx]);
    }

    mbedtls_pk_init(&rsa);

    if( ( ret = mbedtls_pk_parse_key (&rsa, private_key_project, private_key_project_size, 0, 0)) != 0 )
    {
        printf("mbedtls_pk_parse_key error: %d\n", ret);
        return -1;
    }

    char* ciphered_str = "2e0b23f581eada27cbf1f8f61e9ea6b332d73474334e798f58eb31e3a79b1c6c6644485d8d84728fb1203605d7393dd40781a683a4ff89443bee8f6981eb94b917a409d72e6e8d6147c181286dbe3b378ceb2c557081fc760f80b1544c75719614cdd3c226325598746d91f8b71265175d6cfb72fd74582bf61c4b2c2116e908169601b7e785cd8beaa816e68749b45053094ef2b9a587a79ace2f111c12d8ef932a936a8cc48c78203bc0fc693a0faba6e092f114c24599aa69cea89c672996d484f17805373cf88207bd0d7d79f1a3ded23480be0fcacb19b6e7a6cb5f19a97ee6462bdf5d39b0b54792ddc08f321a8888586586e8e294c465741fe74c2ea2";
    size_t ciphered_size = strlen(ciphered_str)/2;
    unsigned char ciphered[ciphered_size];
    unsigned char plain_text[32];
    size_t len_plain_text;

    for (size_t idx = 0; idx < ciphered_size; idx++) {
        sscanf(&ciphered_str[idx*2], "%2hhx", &ciphered[idx]);
    }

    if( ( ret = mbedtls_pk_decrypt (&rsa, ciphered, ciphered_size, plain_text, &len_plain_text, sizeof(plain_text), 0, 0)) != 0 )
    {
        printf("mbedtls_pk_decrypt error: %d\n", ret);
        return -1;
    }

    plain_text[len_plain_text] = '\0';
    printf("%s\n", plain_text);

}

#endif

#if defined(ECDH)

int main(int argc, char *argv[])
{
    mbedtls_ecdh_context ecdh;
    const mbedtls_ecp_curve_info *curve_info;
    int ret;

    // first byte need to be 04 (uncompressed identification) !!!
    char* public_key_author_str = "0404664874f53f5891ad158be8eabe2a731c999a740e2c7cc60ed1fdf8a4a78a953211d974aedb08146be6de87405cb8f6e2f6595e983607b5598454a9f943f77b";
    size_t public_key_author_size = strlen(public_key_author_str)/2;
    unsigned char public_key_author[public_key_author_size];

    for (size_t idx = 0; idx < public_key_author_size; idx++) {
        sscanf(&public_key_author_str[idx*2], "%2hhx", &public_key_author[idx]);
    }

    char* private_key_project_str = "6a3f921d7e1c7689cddb60db226fbd58d663af01a89b2caa8aa8c0f4a6c00223";
    size_t private_key_project_size = strlen(private_key_project_str)/2;
    unsigned char private_key_project[private_key_project_size];

    for (size_t idx = 0; idx < private_key_project_size; idx++) {
        sscanf(&private_key_project_str[idx*2], "%2hhx", &private_key_project[idx]);
    }

    curve_info = mbedtls_ecp_curve_info_from_grp_id(CURVE);
    mbedtls_ecdh_init( &ecdh );
    mbedtls_ecp_group_load( &ecdh.grp, curve_info->grp_id );

    if( ( ret = mbedtls_ecp_point_read_binary( &ecdh.grp, &ecdh.Q, public_key_author, public_key_author_size)) != 0 )
    {
        printf("mbedtls_ecp_point_read_binary error: %d\n", ret);
        return -1;
    }

    if( ( ret = mbedtls_mpi_read_binary( &ecdh.d, private_key_project, private_key_project_size)) != 0 )
    {
        printf("mbedtls_mpi_read_binary error: %d\n", ret);
        return -1;
    }

    mbedtls_mpi shared_secret_mpi;
    mbedtls_mpi_init(&shared_secret_mpi);

    if( ( ret = mbedtls_ecdh_compute_shared( &ecdh.grp, &shared_secret_mpi, &ecdh.Q, &ecdh.d, 0, 0)) != 0 )
    {
        printf("mbedtls_ecdh_compute_shared error: %d\n", ret);
        return -1;
    }

    unsigned char shared_secret[32];

    if( ( ret = mbedtls_mpi_write_binary(&shared_secret_mpi, shared_secret, sizeof (shared_secret))) != 0 )
    {
        printf("mbedtls_mpi_write_binary error: %d\n", ret);
        return -1;
    }

    printf("shared secret: ");
    for (int i = 0; i < sizeof (shared_secret); i++)
    {
        printf("%02x", shared_secret[i]);
    }
    printf("\n");



}

#endif

#if defined(ECDSA_SIGN)

int main(int argc, char *argv[])
{
    int ret = 1;
    unsigned char hash[32];
    unsigned char message[3];

    memcpy(message, "aui", 3);

    // first byte need to be 04 (uncompressed identification) !!!
    char* pubkey_str = "04164639549dc15abf38e6bfa2a4b3cab13cf2820bccdb76fe58507c746b48f174bb3e1c1e54a6865c00e8e90e3349549ddeef7139ef134e9fa30c37652e3951c1";

    // signature need to be formated in der format
    char* signature_str = "3045022100ced1c6cb5b402a3b66898f04bc5627282f9815b09d8f827014f498579c770c8e022054e193c155672ac59cfbb7649bb98b55528251926fe2b76c835d398e4c0aa0b9";

    mbedtls_ecdsa_context ctx_verify;
    const mbedtls_ecp_curve_info *curve_info;

    size_t pubkey_size = strlen(pubkey_str)/2;
    size_t signature_size = strlen(signature_str)/2;

    printf("pubkey_size: %d \n", pubkey_size);

    unsigned char pubkey[pubkey_size];
    unsigned char signature[signature_size];

    for (size_t idx = 0; idx < pubkey_size; idx++) {
        sscanf(&pubkey_str[idx*2], "%2hhx", &pubkey[idx]);
    }

    for (size_t idx = 0; idx < signature_size; idx++) {
        sscanf(&signature_str[idx*2], "%2hhx", &signature[idx]);
    }

    mbedtls_ecdsa_init( &ctx_verify );

    if( ( ret = mbedtls_sha256_ret( message, sizeof( message ), hash, 0 ) ) != 0 )
    {
        printf( " failed\n  ! mbedtls_sha256_ret returned %d\n", ret );
        goto exit;
    }

    printf("\n");

    curve_info = mbedtls_ecp_curve_info_from_grp_id(CURVE);
    mbedtls_ecp_group_load(&ctx_verify.grp, curve_info->grp_id);

    if( ( ret = mbedtls_ecp_point_read_binary( &ctx_verify.grp, &ctx_verify.Q, pubkey, pubkey_size)) != 0 )
    {
        printf("mbedtls_ecp_point_read_binary error: %d\n", ret);
        goto exit;
    }

    if( ( ret = mbedtls_ecdsa_read_signature( &ctx_verify, hash, sizeof( hash ), signature, signature_size ) ) != 0 )
    {
        printf( " failed\n  ! mbedtls_ecdsa_read_signature returned %d\n", ret );
        goto exit;
    }

    printf( " ok\n" );

exit:

    mbedtls_ecdsa_free( &ctx_verify );

    return -1;
}

#endif


#if defined(ECDSA)

static void dump_buf( const char *title, unsigned char *buf, size_t len )
{
    size_t i;

    printf( "%s", title );
    for( i = 0; i < len; i++ )
    {
        printf("%c%c", "0123456789ABCDEF" [buf[i] / 16],
                       "0123456789ABCDEF" [buf[i] % 16] );
    }

    printf( "\n" );
}

static void dump_pubkey( const char *title, mbedtls_ecdsa_context *key )
{
    unsigned char buf[300];
    size_t len;

    if( mbedtls_ecp_point_write_binary( &key->grp, &key->Q,
                MBEDTLS_ECP_PF_UNCOMPRESSED, &len, buf, sizeof buf ) != 0 )
    {
        printf("internal error\n");
        return;
    }

    dump_buf( title, buf, len );


}

int main(int argc, char *argv[])
{
    int ret = 1;
    int exit_code = -1;
    mbedtls_ecdsa_context ctx_sign, ctx_verify;
    mbedtls_entropy_context entropy;
    mbedtls_ctr_drbg_context ctr_drbg;
    unsigned char message[3];
    unsigned char hash[32];
    unsigned char sig[MBEDTLS_ECDSA_MAX_LEN];
    size_t sig_len;
    const char *pers = "ecdsa";
    ((void) argv);

    mbedtls_ecdsa_init( &ctx_sign );
    mbedtls_ecdsa_init( &ctx_verify );
    mbedtls_ctr_drbg_init( &ctr_drbg );

    memset( sig, 0, sizeof( sig ) );
    memcpy(message, "aui", 3);

    /*
    * Generate a key pair for signing
    */
    printf( "\n  . Seeding the random number generator..." );
    fflush( stdout );

    mbedtls_entropy_init( &entropy );
    if( ( ret = mbedtls_ctr_drbg_seed( &ctr_drbg, mbedtls_entropy_func, &entropy,
                               (const unsigned char *) pers,
                               strlen( pers ) ) ) != 0 )
    {
        printf( " failed\n  ! mbedtls_ctr_drbg_seed returned %d\n", ret );
        goto exit;
    }

    printf( " ok\n  . Generating key pair..." );
    fflush( stdout );

    if( ( ret = mbedtls_ecdsa_genkey( &ctx_sign, CURVE, mbedtls_ctr_drbg_random, &ctr_drbg ) ) != 0 )
    {
        printf( " failed\n  ! mbedtls_ecdsa_genkey returned %d\n", ret );
        goto exit;
    }

    printf( " ok (key size: %d bits)\n", (int) ctx_sign.grp.pbits );

    dump_pubkey( "  + Public key: ", &ctx_sign );

    /*
     * Compute message hash
     */
    printf( "  . Computing message hash..." );
    fflush( stdout );

    if( ( ret = mbedtls_sha256_ret( message, sizeof( message ), hash, 0 ) ) != 0 )
    {
        printf( " failed\n  ! mbedtls_sha256_ret returned %d\n", ret );
        goto exit;
    }

    printf( " ok\n" );

    dump_buf( "  + Hash: ", hash, sizeof( hash ) );

    /*
     * Sign message hash
     */
    printf( "  . Signing message hash..." );
    fflush( stdout );

    if( ( ret = mbedtls_ecdsa_write_signature( &ctx_sign, MBEDTLS_MD_SHA256,
                                       hash, sizeof( hash ),
                                       sig, &sig_len,
                                       mbedtls_ctr_drbg_random, &ctr_drbg ) ) != 0 )
    {
        printf( " failed\n  ! mbedtls_ecdsa_write_signature returned %d\n", ret );
        goto exit;
    }
    printf( " ok (signature length = %u)\n", (unsigned int) sig_len );

    dump_buf( "  + Signature: ", sig, sig_len );

    /*
     * Transfer public information to verifying context
     *
     * We could use the same context for verification and signatures, but we
     * chose to use a new one in order to make it clear that the verifying
     * context only needs the public key (Q), and not the private key (d).
     */
    printf( "  . Preparing verification context..." );
    fflush( stdout );

    if( ( ret = mbedtls_ecp_group_copy( &ctx_verify.grp, &ctx_sign.grp ) ) != 0 )
    {
        printf( " failed\n  ! mbedtls_ecp_group_copy returned %d\n", ret );
        goto exit;
    }

    if( ( ret = mbedtls_ecp_copy( &ctx_verify.Q, &ctx_sign.Q ) ) != 0 )
    {
        printf( " failed\n  ! mbedtls_ecp_copy returned %d\n", ret );
        goto exit;
    }

    /*
     * Verify signature
     */
    printf( " ok\n  . Verifying signature..." );
    fflush( stdout );

    if( ( ret = mbedtls_ecdsa_read_signature( &ctx_verify,
                                      hash, sizeof( hash ),
                                      sig, sig_len ) ) != 0 )
    {
        printf( " failed\n  ! mbedtls_ecdsa_read_signature returned %d\n", ret );
        goto exit;
    }

    printf( " ok\n" );

exit:

    mbedtls_ecdsa_free( &ctx_verify );
    mbedtls_ecdsa_free( &ctx_sign );
    mbedtls_ctr_drbg_free( &ctr_drbg );
    mbedtls_entropy_free( &entropy );

    return exit_code;
}
#endif
