namespace py application.thrifts.services.types
namespace java application.thrifts.services.types
namespace go application.thrifts.services.types

typedef string UserID

struct UserInfo {
    10: string first_name
    20: string last_name
}
