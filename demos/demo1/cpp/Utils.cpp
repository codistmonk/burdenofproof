// NOLINT(legal/copyright)
#include <boost/filesystem.hpp>
#include <cassert>
#include <fstream>  // NOLINT(readability/streams)
#include <string>
#include <sstream>
#include <vector>
#include "Utils.hpp"
#include "Maths.hpp"

#define FEMALE_NAMES\
    "../../name/word_list_moby_given_names_english_female.flat.txt"
#define MALE_NAMES\
    "../../name/word_list_moby_given_names_english_male.flat.txt"
#define LAST_NAMES\
    "../../name/word_list_moby_given_names_english.flat.txt"

using utils::NameFactory;

NameFactory::NameFactory() {
    std::string line;
    std::ifstream femaleNamesFile(FEMALE_NAMES, std::ios::in);

    while (femaleNamesFile >> line) {
        m_femaleFirstNames.push_back(std::move(line));
    }

    m_femaleFirstNameCount = m_femaleFirstNames.size();

    SHOW(m_femaleFirstNameCount);

    std::ifstream maleNamesFile(MALE_NAMES, std::ios::in);

    while (maleNamesFile >> line) {
        m_maleFirstNames.push_back(std::move(line));
    }

    m_maleFirstNameCount = m_maleFirstNames.size();

    SHOW(m_maleFirstNameCount);

    std::ifstream namesFile(LAST_NAMES, std::ios::in);

    while (namesFile >> line) {
        m_lastNames.push_back(std::move(line));
    }

    m_NameCount = m_lastNames.size();

    SHOW(m_NameCount);
}

NameFactory::~NameFactory() {}

std::string const & NameFactory::randomMaleName() {
    static maths::RandomIntGenerator rnd(0, m_maleFirstNameCount - 1);

    return m_maleFirstNames[rnd()];
}

std::string const & NameFactory::randomFemaleName() {
    static maths::RandomIntGenerator rnd(0, m_femaleFirstNameCount - 1);

    return m_femaleFirstNames[rnd()];
}

std::string const & NameFactory::randomLastName() {
    static maths::RandomIntGenerator rnd(0, m_NameCount - 1);

    return m_lastNames[rnd()];
}


std::string utils::fileToStdString(
        const boost::filesystem::path &path) {
    using boost::filesystem::exists;
    using boost::filesystem::is_regular_file;

    assert(exists(path));
    assert(is_regular_file(path));
    std::ifstream file(path.string(),
                       std::ifstream::binary);
    assert(file.is_open());
    file.seekg(0, file.end);
    std::int64_t length = file.tellg();
    file.seekg(0, file.beg);
    file.clear();
    std::vector<char> buffer(length);
    file.read(&buffer[0], length);
    assert(file);
    std::string RES(&buffer[0], length);
    return RES;
}
