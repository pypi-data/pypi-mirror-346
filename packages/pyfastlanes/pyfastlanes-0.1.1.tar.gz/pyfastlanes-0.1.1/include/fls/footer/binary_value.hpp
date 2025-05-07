#ifndef FLS_FOOTER_BINARY_VALUE_HPP
#define FLS_FOOTER_BINARY_VALUE_HPP

#include "fls/std/vector.hpp"

namespace fastlanes {
/*--------------------------------------------------------------------------------------------------------------------*\
 * BinaryValue
\*--------------------------------------------------------------------------------------------------------------------*/
class BinaryValue {
public:
	BinaryValue() = default;

public:
	vector<std::byte> binary_data;
};

} // namespace fastlanes
#endif // FLS_FOOTER_BINARY_VALUE_HPP
