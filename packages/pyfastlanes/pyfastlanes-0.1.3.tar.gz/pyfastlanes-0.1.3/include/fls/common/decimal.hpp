#ifndef FLS_COMMON_DECIMAL_HPP
#define FLS_COMMON_DECIMAL_HPP

#include "fls/common/common.hpp"

namespace fastlanes {

class DecimalType {
public:
	DecimalType();
	DecimalType(n_t precision, n_t scale);

	// Total number of digits (integer + fraction)
	n_t precision;
	// Number of digits after the decimal point
	n_t scale;
};

int64_t     make_decimal(const std::string& value, n_t scale);
DecimalType make_decimal_t(const std::string& value);

} // namespace fastlanes

#endif // FLS_COMMON_DECIMAL_HPP
