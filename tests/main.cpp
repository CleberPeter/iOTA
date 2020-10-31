#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cstddef>

#include <mbedtls/ecdsa.h>
#include <mbedtls/sha256.h>
#include <mbedtls/entropy.h>
#include <mbedtls/ctr_drbg.h>

using namespace std;

#define CURVE MBEDTLS_ECP_DP_SECP256K1

// private_key c7e6a38fe004a1a7a5cc4240c799c7511de604df618cdf7d0f7b28eeefef58cf

#define SIGN

#ifdef SIGN

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


#else
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
