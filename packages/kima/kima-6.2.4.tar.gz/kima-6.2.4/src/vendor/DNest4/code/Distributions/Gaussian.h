#ifndef DNest4_Gaussian
#define DNest4_Gaussian

#include <limits>
#include "ContinuousDistribution.h"
#include "../RNG.h"
#include "../Utils.h"

namespace DNest4
{

class Gaussian:public ContinuousDistribution
{
    private:
        const double _norm_pdf_logC = log(sqrt(2 * M_PI));

    public:
        // Location and scale parameter
        double center, width;

        Gaussian(double center=0.0, double width=1.0);

        double cdf(double x) const override;
        double cdf_inverse(double p) const override;
        double log_pdf(double x) const override;

        virtual std::ostream& print(std::ostream& out) const override
        {
            out << "Gaussian(" << center << "; " << width << ")";
            return out;
        }
};


class HalfGaussian:public ContinuousDistribution
{
    private:
        const double _halfnorm_pdf_logC = log(sqrt(2 / M_PI));

    public:
        // scale parameter
        double width;

        HalfGaussian(double width=1.0);

        double cdf(double x) const override;
        double cdf_inverse(double p) const override;
        double log_pdf(double x) const override;

        virtual std::ostream& print(std::ostream& out) const override
        {
            out << "HalfGaussian(" << width << ")";
            return out;
        }
};

class TruncatedGaussian:public ContinuousDistribution
{
    private:
        const double _norm_pdf_logC = log(sqrt(2 * M_PI));

    public:
        // Location and scale parameter
        double center, width;
        double lower, upper;
        double alpha, beta, Z;

        TruncatedGaussian(double center=0.0, double width=1.0,
                          double lower=-std::numeric_limits<double>::infinity(),
                          double upper=std::numeric_limits<double>::infinity());

        double cdf(double x) const override;
        double cdf_inverse(double p) const override;
        double log_pdf(double x) const override;

        virtual std::ostream& print(std::ostream& out) const override
        {
            out << "TruncatedGaussian(" << center << "; " << width << "; [" << lower << ", " << upper << "])";
            return out;
        }
};


} // namespace DNest4

#endif

